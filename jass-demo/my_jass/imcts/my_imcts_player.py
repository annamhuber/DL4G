# HSLU
#
# Created by Flavio Lazzarini on 30.09.18
# Test
#

from jass.base.const import*
from jass.base.player_round_cheating import PlayerRound
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.round_factory import get_round_from_player_round
from jass.player.player_cheating import Player

from my_jass.imcts.sampler import Sampler
from my_jass.mcts.node import Node
from my_jass.mcts.tree import Tree
from my_jass.mcts.UCB import UCB
from my_jass.player.my_player import MyPlayer
from tensorflow.keras.models import load_model
import time
from jass.player.random_player_schieber import RandomPlayerSchieber

class MyIMCTSPlayer(Player):

    def __init__(self):
        self.model = load_model('models/final_bot_trump_model_V4.h5')
    """
    Implementation of a player to play Jass using Minimax.
    """
    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest number of cards
        if rnd.forehand is None:
            forehand = 0
        else:
            forehand = 1
        arr = np.array([np.append(rnd.hand, forehand)])
        trump = self.model.predict(arr)

        return np.argmax(trump)

    def play_card(self, rnd: PlayerRound) -> int:
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

    def montecarlotreesearch(self, rnd: PlayerRound):
        sampled_rnd = Sampler.sample(rnd)
        tree = Tree()
        rootNode = tree.getRootNode()
        rootNode.getAction().setPlayerNr(rnd.player)
        rootNode.getAction().setRound(sampled_rnd)

        t_end = time.time() + 0.02
        while time.time() < t_end:
            promisingNode = self.selectPromisingNode(rootNode)
            if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                self.expandNode(promisingNode, sampled_rnd)

            nodeToExplore = promisingNode
            if len(promisingNode.getChilds()) > 0:
                nodeToExplore = promisingNode.getRandomChild()

            winScore = self.simulateRound(nodeToExplore)
            self.backPropagation(nodeToExplore, sampled_rnd.player, winScore)
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
        randomPlayer = RandomPlayerSchieber()
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
