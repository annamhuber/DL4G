# HSLU
#
# Created by Flavio Lazzarini on 30.09.18
#

import logging
from jass.base.const import JASS_SCHIEBER_1000
from jass.arena.arena_cheating import ArenaCheating
from jass.arena.trump_selection_players_strategy import TrumpPlayerStrategy
from jass.arena.play_game_nr_rounds_strategy import PlayNrRoundsStrategy
from jass.player.random_player_schieber import RandomPlayerSchieber

from my_jass.minimax.my_minimax_player import MyMinimaxPlayer
from my_jass.minimax.my_alphabeta_player import MyAlphaBetaPlayer
from my_jass.minimax.minimax_player_kevin import MinimaxPlayerKevin

from my_jass.mcts.my_mcts_player import MyMCTSPlayer

def main():
    # Set the global logging level (Set to debug or info to see more messages)
    logging.basicConfig(level=logging.WARNING)

    # setup the arena
    arena = ArenaCheating(jass_type=JASS_SCHIEBER_1000,
                  trump_strategy=TrumpPlayerStrategy(),
                  play_game_strategy=PlayNrRoundsStrategy(4))
    player = RandomPlayerSchieber()
    #player = MyMCTSPlayer()

    #set my player
    #my_player = MyMinimaxPlayer()
    my_player = MyMCTSPlayer()

    arena.set_players(my_player, player, my_player, player)
    arena.nr_games_to_play = 10
    print('Playing {} games'.format(arena.nr_games_to_play))
    arena.play_all_games()
    total_games = arena.nr_wins_team_0 + arena.nr_wins_team_1 + arena.nr_draws
    print('Wins Team 0: {} ({:.2f}%)'.format(arena.nr_wins_team_0, arena.nr_wins_team_0 / total_games))
    print('Wins Team 1: {} ({:.2f}%)'.format(arena.nr_wins_team_1, arena.nr_wins_team_1 / total_games))
    print('Draws: {} ({:.2f}%)'.format(arena.nr_draws, arena.nr_draws / total_games))
    print('Delta Points: {}'.format(arena.delta_points))


if __name__ == '__main__':
    main()
