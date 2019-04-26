# HSLU
#
# Created by Thomas Koller on 06.09.18
#
import logging
import numpy as np

from jass.base.const import JASS_HEARTS, color_masks, HEARTS, card_strings
from jass.base.player_round import PlayerRound
from jass.player.player import Player


class MyPlayerHearts(Player):
    """
    Simple example of a player to play hearts.
    """
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def select_trump(self, rnd: PlayerRound) -> int or None:
        """
        There is no trump in heart, but we must implement the method as the Player interface is independent of
        the jass type
        Args:
            rnd: not used
        Returns:
            None
        """
        return None

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Implement the action to play hearts.
        Args:
            rnd: The round for which to play
        Returns:
            the card to play, must be a valid card
        """
        # we can check if we are playing the correct game
        assert rnd.jass_type == JASS_HEARTS

        # get the valid cards to play
        valid_cards = rnd.get_valid_cards()

        # lets divide our cards into heart and other cards
        my_heart_cards = valid_cards * color_masks[HEARTS, :]
        my_other_cards = valid_cards - my_heart_cards

        if rnd.nr_cards_in_trick == 0:
            # we are the first player, so we can select what to play
            # lets select some random non-heart card if we have any (not that this is necessarily
            # a good strategy :-)
            if my_other_cards.sum() > 0:
                card = np.random.choice(np.flatnonzero(my_other_cards))
            else:
                # just play a random valid card
                card = np.random.choice(np.flatnonzero(valid_cards))
        else:
            # if we have to give a card, lets try to give a heart card
            if my_heart_cards.sum() > 0:
                card = np.random.choice(np.flatnonzero(my_heart_cards))
            else:
                # just play a random valid card
                card = np.random.choice(np.flatnonzero(valid_cards))

        self._logger.debug('Played card: {}'.format(card_strings[card]))
        return card




