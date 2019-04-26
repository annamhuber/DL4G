# HSLU
#
# Created by Thomas Koller on 20.08.18
#

import numpy as np

from jass.base.const import color_masks
from jass.base.player_round import PlayerRound
from jass.player.player import Player
from tensorflow.keras.models import load_model



class MyPlayerDeepTrump(Player):
    """
    Sample implementation of a player to play Jass.
    """

    def __init__(self):

        self.model = load_model('models/final_bot_trump_model_V4.h5')
        self.model._make_predict_function()

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
        # play random

        # get the valid cards to play
        trump = rnd.declared_trump;
        valid_cards = rnd.get_valid_cards()

        # select a random card
        return np.random.choice(np.flatnonzero(valid_cards))
