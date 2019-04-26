
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
import random
import os

class MyMLPlayer(Player):

    def __init__(self, model_trump = None, model_card = None):
        if model_trump is None:
            self.model = load_model('models/final_bot_trump_model_V4.h5')

        else:
            self.model = model_trump

        self.model._make_predict_function()
        if model_card is None:
            self.card_model = load_model('models/final_bot_model_V6.h5')
        else:
            self.card_model = model_card

        self.card_model._make_predict_function()
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
        bestcard = self.card_model.predict(np.array([self.create_array(rnd)]))
        # print(np.array([self.create_array(rnd)]))

        return np.argmax(bestcard)

    def create_array(self, player_rnd: PlayerRound) -> np.array:
        start_trick = time.time()
        cards_played_in_round = np.zeros([36], np.int)
        for trick_id in range(player_rnd.nr_tricks):
            for i in range(4):
                cards_played_in_round[player_rnd.tricks[trick_id, i]] = 1.0

        # print("trick1 %.10f" % (time.time() - start_trick))
        # 36 elements
        # convert hand by player

        hand = player_rnd.hand.astype(np.int)
        # 36 elements

        declare_trump = self.one_hot(player_rnd.declared_trump, 4)
        # 4 elements

        forehand = np.asarray([player_rnd.forehand], dtype=np.int)
        # 1 element

        trump = self.one_hot(player_rnd.trump, 6)
        # 6 elements

        start_player_tricks = time.time()
        # cards played in trick, 1 hot encoded
        if player_rnd.nr_cards_in_trick > 0:
            first_card = self.one_hot(player_rnd.current_trick[0], 36)
        else:
            first_card = np.zeros(36, dtype=np.int)
        if player_rnd.nr_cards_in_trick > 1:
            second_card = self.one_hot(player_rnd.current_trick[1], 36)
        else:
            second_card = np.zeros(36, dtype=np.int)
        if player_rnd.nr_cards_in_trick > 2:
            third_card = self.one_hot(player_rnd.current_trick[2], 36)
        else:
            third_card = np.zeros(36, dtype=np.int)
        # 108 elements

        # print("trick2 %.10f" % (time.time()- start_player_tricks))
        return np.concatenate([cards_played_in_round, hand, declare_trump, forehand, trump,
                               first_card, second_card, third_card], axis=0)

    def one_hot(self, number, size) -> np.array:
        """
        One hot encoding for a single value. Output is float array of size size
        Args:
            number: number to one hot encode
            size: length of the returned array
        Returns:
            array filled with 0.0 where index != number and 1.0 where index == number
        """
        result = np.zeros(size, dtype=np.int)
        result[number] = 1
        return result