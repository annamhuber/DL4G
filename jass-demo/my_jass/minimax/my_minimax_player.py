# HSLU
#
# Created by Flavio Lazzarini on 30.09.18
# Test
#

from jass.base.const import*
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.player.player_cheating import PlayerCheating
from jass.base.rule_schieber import RuleSchieber
import sys


class MyMinimaxPlayer(PlayerCheating):
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
        playerRound = PlayerRoundCheating()
        playerRound.set_from_round(rnd)

        cardToPlay = self.minimax(playerRound, 0, True)

        return cardToPlay[0]

    def minimax(self, rnd: PlayerRoundCheating, lastCard: int, maximizingPlayer: bool)-> (int, int):
        """
        Returns the best card to play, based on the minimax algorithm

        Args:
            rnd: For the first call this is the current round. For further calls inside the recursion this ist the round that is being simulated
            lastCard: the last Card that has been played
            maximizingPlayer: if you need to maximize or minimize
        Returns:
            the best card to play, int encoded
        """
        bestValue = 0
        bestCard = (0,0)
        if rnd.nr_cards_in_trick > 3:
            rule = RuleSchieber()
            points = rule.calc_points(rnd.current_trick, rnd.nr_played_cards == 36, rnd.trump)
            winner = rule.calc_winner(rnd.current_trick, rnd.trick_first_player[rnd.nr_tricks], rnd.trump)
            if winner == NORTH or winner == SOUTH:
                bestCard = (lastCard, points)
            else:
                bestCard = (lastCard, -points)
        elif maximizingPlayer:
            bestValue = -sys.maxsize
            cardsToPlay = np.flatnonzero(rnd.get_valid_cards())
            for card in cardsToPlay:
                newRound = self.fakeMove(rnd, card)
                childCard = self.minimax(newRound, card, False)
                if bestValue < childCard[1]:
                    bestValue = childCard[1]
                    bestCard = childCard
        else:
            bestValue = sys.maxsize
            cardsToPlay = np.flatnonzero(rnd.get_valid_cards())
            for card in cardsToPlay:
                newRound = self.fakeMove(rnd, card)
                childCard = self.minimax(newRound, card, True)
                if bestValue > childCard[1]:
                    bestValue = childCard[1]
                    bestCard = childCard

        return bestCard

    def fakeMove(self, rnd: PlayerRoundCheating, cardToPlay: int)->PlayerRoundCheating:
        nextRound = PlayerRoundCheating()
        nextRound.set_from_round(rnd)
        nextRound.current_trick[rnd.nr_cards_in_trick] = cardToPlay
        nextRound.hands[nextRound.player, cardToPlay] = 0
        nextRound.nr_cards_in_trick = nextRound.nr_cards_in_trick + 1
        nextRound.nr_played_cards = nextRound.nr_played_cards + 1
        nextRound.player = (nextRound.player - 1) % 4

        nextRound.hand = nextRound.hands[nextRound.player]
        return nextRound
