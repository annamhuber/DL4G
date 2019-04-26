from jass.base.const import *
from jass.base.player_round_cheating import PlayerRound
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.round_factory import get_round_from_player_round
import random


class Sampler:

    @staticmethod
    def sample(rnd: PlayerRound) -> PlayerRoundCheating:
        my_hand = np.flatnonzero(rnd.hand)
        sampledCards = np.zeros(shape=36, dtype=np.int)
        sampledCards.fill(1)
        for i in my_hand:
            sampledCards[i] = 0

        hands = np.zeros(shape=[4, 36], dtype=np.int)

        # Komischerweise spielt er mit random hands besser
        hands1, sampledCards = Sampler.__get_hands(sampledCards)

        hands2, sampledCards = Sampler.__get_hands(sampledCards)

        hands3, sampledCards = Sampler.__get_hands(sampledCards)

        hands[0] = hands1
        hands[1] = hands2
        hands[2] = rnd.hand
        hands[3] = hands3

        # anhand des Spielers die hand richtig setzen
        # for j in range(0,4):
        #     if j == rnd.player:
        #         hands[j] = rnd.hand
        #     else:
        #         hands1, sampledCards = Sampler.__get_hands(sampledCards)
        #         hands[j] = hands1

        return get_round_from_player_round(rnd, hands)
    @staticmethod
    def __get_hands(sampled_cards: np.array):
        handsplayer1 = np.zeros(shape=36, dtype=int)
        for i in range(0, 9):
            card = random.choice(np.flatnonzero(sampled_cards))
            sampled_cards[card] = 0
            handsplayer1[card] = 1

        return handsplayer1, sampled_cards
