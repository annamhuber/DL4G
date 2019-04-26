# HSLU
#
# Created by Flavio Lazzarini on 30.09.18
# Test
#

from jass.base.const import*
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.round_factory import get_round_from_player_round
from jass.player.player_cheating import PlayerCheating
from jass.base.rule_schieber import RuleSchieber

from my_jass.mcts.const import Status
from my_jass.mcts.node import Node
from my_jass.mcts.tree import Tree
from my_jass.mcts.UCB import UCB
from my_jass.player.my_player import MyPlayer
import time

class MyMCTSPlayer(PlayerCheating):
    """
    Implementation of a player to play Jass using Minimax.
    """
    def select_trump(self, rnd: PlayerRoundCheating) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest number of cards
        trump = 0
        max_number_in_color = 0
        for c in range(4):
            number_in_color = (rnd.hand * color_masks[c]).sum()
            if number_in_color > max_number_in_color:
                max_number_in_color = number_in_color
                trump = c
        return trump

    def play_card(self, rnd: PlayerRoundCheating) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded
        """
        #Create Simulation stuff
        #simRound = get_round_from_player_round(rnd, rnd.hands)
        bestcard = self.montecarlotreesearch(rnd)

        return bestcard

    def montecarlotreesearch(self, rnd: PlayerRoundCheating):
        tree = Tree()
        rootNode = tree.getRootNode()
        rootNode.getAction().setPlayerNr(rnd.player)
        rootNode.getAction().setRound(rnd)

        t_end = time.time() + 0.02
        while time.time() < t_end:
            promisingNode = self.selectPromisingNode(rootNode)
            if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                self.expandNode(promisingNode, rnd)

            nodeToExplore = promisingNode
            if len(promisingNode.getChilds()) > 0:
                nodeToExplore = promisingNode.getRandomChild()

            winScore = self.simulateRound(nodeToExplore)
            self.backPropagation(nodeToExplore, rnd.player, winScore)
        winner = rootNode.getChildWithMaxVisitCount().getAction().getCard()
        return winner

    def selectPromisingNode(self, rootNode: Node)->Node:
        node = rootNode
        while len(node.getChilds()) != 0:
            ucb = UCB()
            node = ucb.findBestNoteUCB(node)
        return node


    def expandNode(self, node:Node, rnd: PlayerRoundCheating):
        validCards =  np.flatnonzero(rnd.get_valid_cards())
        for card in validCards:
            newNode = Node()
            newNode.setParent(node)
            newNode.getAction().setRound(rnd)
            newNode.getAction().setPlayerNr(node.getAction().getRound().player)
            newNode.getAction().setCard(card)
            node.addChild(newNode)

    def simulateRound(self, node: Node):
        rnd = get_round_from_player_round(node.getAction().getRound(), node.getAction().getRound().hands)
        rnd.action_play_card(node.getAction().getCard())
        cards = rnd.nr_played_cards
        randomPlayer = MyPlayer()
        while cards < 36:
            player_rnd = PlayerRoundCheating()
            player_rnd.set_from_round(rnd)
            card_action = randomPlayer.play_card(player_rnd)
            rnd.action_play_card(card_action)
            cards += 1


        myPoints = rnd.points_team_0
        pointsEnemy = rnd.points_team_1
        maxPoints = myPoints + pointsEnemy

        if myPoints > pointsEnemy:
            return (myPoints - 0) / (maxPoints - 0)
        else:
            return 0

    def backPropagation(self, node: Node, playerNr: int, winScore: int):
        tempNode = node
        while tempNode != None:
            tempNode.getAction().incrementVisit()
            if tempNode.getAction().getPlayerNr() == playerNr:
                tempNode.getAction().setWinScore(winScore)
            tempNode = tempNode.getParent()
