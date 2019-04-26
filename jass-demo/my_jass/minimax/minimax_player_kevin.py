# HSLU
#
# Created by Thomas Koller on 20.08.18
#

import numpy as np
from typing import List

from jass.base.const import color_masks
from jass.base.const import card_values
from jass.base.round import Round
from jass.base.player_round import PlayerRound
from jass.base.player_round_cheating import  PlayerRoundCheating
from jass.player.player_cheating import PlayerCheating
from jass.base.rule_schieber import RuleSchieber



class MinimaxPlayerKevin(PlayerCheating):
    """
    Sample implementation of a player to play Jass.
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
        # play random

        # get the valid cards to play
        valid_cards = rnd.get_valid_cards()

        value_of_hand = self.get_value_of_hand(rnd)


        # select a random card
        cardToPlay = self.minimax_recursive(rnd)
        return cardToPlay

    def get_value_of_hand(self, rnd: PlayerRoundCheating) -> np.array:
        hand = rnd.hand
        for i in range(hand.size):
            if hand[i] == 1:
                hand[i] = card_values[rnd.trump, i]

        return hand

    def  getIndexOfValidCardWithHighestValue(self, rnd: PlayerRoundCheating) -> int:
        hand = rnd.hand
        indexOfCardToReturn = 0
        highestValue = 0
        for i in range(hand.size):
            if hand[i] == 1 and card_values[rnd.trump, i] >= highestValue:
                indexOfCardToReturn = i
                highestValue = card_values[rnd.trump, i]

        return indexOfCardToReturn

    def  getIndexOfValidCardWithLowestValue(self, rnd: PlayerRoundCheating) -> int:
        hand = rnd.hand
        indexOfCardToReturn = 0
        lowestValue = 1000
        for i in range(hand.size):
            if hand[i] == 1 and card_values[rnd.trump, i] <= lowestValue:
                indexOfCardToReturn = i
                lowestValue = card_values[rnd.trump, i]

        return indexOfCardToReturn

    def  getHighestValueInHand(self, rnd: PlayerRoundCheating) -> np.array:
        hand = rnd.hand
        # Array[0] -> Index of Card, Array[1] -> Value of Card
        # ToDo: Refactor later to Container
        returnArray = np.zeros(shape=[2], dtype=np.int32)

        for i in range(hand.size):
            if hand[i] == 1 and card_values[rnd.trump, i] >= returnArray[1]:
                returnArray[1] = card_values[rnd.trump, i]
                returnArray[0] = i

        return returnArray

    def minimax_recursive(self, rnd: PlayerRoundCheating) -> int:

        rndCopy = PlayerRoundCheating()
        rndCopy.set_from_round(rnd)

        returnValue = self.minimax_recursive2(rndCopy, False)
        return returnValue[1]



    def minimax_recursive2(self, roundCheating: PlayerRoundCheating, enemyPlayer: bool) -> np.array:

        # playerID = roundCheating.player
        validCards = roundCheating.get_valid_cards()
        returnValues = np.zeros(shape=[2], dtype=np.int32)

        if roundCheating.nr_cards_in_trick >= 3:
            if enemyPlayer:
                returnValues = self.getHighestValueInHand(roundCheating)
                returnValues[1] = (-1)*returnValues[1]
                return returnValues
            else:
                returnValues = self.getHighestValueInHand(roundCheating)
                return returnValues
        else:
            cardValues = np.zeros(shape=[36], dtype=np.int32)
            for i in range(validCards.size):
                if validCards[i] == 1:
                    newRound = self.createFollowingRoundFromTurn(roundCheating, i)
                    cardValues[i] = (self.minimax_recursive2(newRound, not enemyPlayer))[1]

            if enemyPlayer:
                returnValues[0] = np.argmin(cardValues)
                returnValues[1] = cardValues[returnValues[0]]
                return returnValues
            else:
                returnValues[0] = np.argmax(cardValues)
                returnValues[1] = cardValues[returnValues[0]]
                return returnValues

    def createFollowingRoundFromTurn(self, currentRound: PlayerRoundCheating, cardToPlay: int) -> PlayerRoundCheating:
        newRound = PlayerRoundCheating()
        newRound.set_from_round(currentRound)

        newRound.current_trick[newRound.nr_cards_in_trick] = cardToPlay
        newRound.hands[newRound.player, cardToPlay] = 0

        newRound.nr_cards_in_trick = newRound.nr_cards_in_trick+1
        newRound.nr_played_cards = newRound.nr_played_cards+1
        newRound.player = (newRound.player-1) % 4

        newRound.hand = newRound.hands[newRound.player]

        return newRound



