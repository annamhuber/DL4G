# HSLU
#
# Created by Thomas Koller on 20.08.18
#
import logging
from jass.base.const import JASS_HEARTS
from jass.arena.arena import Arena
from jass.arena.trump_selection_none_strategy import TrumpNoneStrategy
from jass.arena.play_game_nr_rounds_strategy import PlayNrRoundsStrategy
from jass.player.random_player_hearts import RandomPlayerHearts
from my_jass.player.my_player_hearts import MyPlayerHearts


def main():
    # Set the global logging level, so that we see more information
    # logging.basicConfig(level=logging.INFO)

    # setup the arena
    arena = Arena(jass_type=JASS_HEARTS,
                  trump_strategy=TrumpNoneStrategy(),
                  play_game_strategy=PlayNrRoundsStrategy(4))
    player = RandomPlayerHearts()
    my_player = MyPlayerHearts()

    arena.set_players(my_player, player, my_player, player)
    arena.nr_games_to_play = 1000
    print('Playing {} games'.format(arena.nr_games_to_play))
    arena.play_all_games()
    total_games = arena.nr_wins_team_0 + arena.nr_wins_team_1 + arena.nr_draws
    print('Wins Team 0: {} ({:.2f}%)'.format(arena.nr_wins_team_0, arena.nr_wins_team_0/total_games))
    print('Wins Team 1: {} ({:.2f}%)'.format(arena.nr_wins_team_1, arena.nr_wins_team_1/total_games))
    print('Draws: {} ({:.2f}%)'.format(arena.nr_draws, arena.nr_draws/total_games))
    print('Delta Points: {}'.format(arena.delta_points))


if __name__ == '__main__':
    main()
