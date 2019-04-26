# HSLU
#
# Created by Thomas Koller on 10.09.18
#
"""
Read swisslos log files and convert them to comma seperated value files for ML.
"""

import os
import csv
import argparse

import numpy as np

from jass.base.const import PUSH, PUSH_ALT, next_player, partner_player
from jass.base.player_round import PlayerRound
from jass.io.log_parser import LogParser

def one_hot(number, size):
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


def calculate_features(player_rnd: PlayerRound):
    """
    Example of converting  player round to array of features. For usage in network, the resulting
    feature vector should be converted to float. It is returned as int for saving in a cvs files.

    Args:
        player_rnd: the player round to convert
    Returns:
        numpy array of features
    """
    # convert played cards in tricks to one hot encoded array (not preserving information who played
    # the card and when
    cards_played_in_round = np.zeros([36], np.int)
    for trick_id in range(player_rnd.nr_tricks):
        for i in range(4):
            cards_played_in_round[player_rnd.tricks[trick_id, i]] = 1.0
    # 36 elements

    # convert hand by player
    hand = player_rnd.hand.astype(np.int)
    # 36 elements

    declare_trump = one_hot(player_rnd.declared_trump, 4)
    # 4 elements

    forehand = np.asarray([player_rnd.forehand], dtype=np.int)
    # 1 element

    trump = one_hot(player_rnd.trump, 6)
    # 6 elements

    # cards played in trick, 1 hot encoded
    if player_rnd.nr_cards_in_trick > 0:
        first_card = one_hot(player_rnd.current_trick[0], 36)
    else:
        first_card = np.zeros(36, dtype=np.int)
    if player_rnd.nr_cards_in_trick > 1:
        second_card = one_hot(player_rnd.current_trick[1], 36)
    else:
        second_card = np.zeros(36, dtype=np.int)
    if player_rnd.nr_cards_in_trick > 2:
        third_card = one_hot(player_rnd.current_trick[2], 36)
    else:
        third_card = np.zeros(36, dtype=np.int)
    # 108 elements

    return np.concatenate([cards_played_in_round, hand, declare_trump, forehand, trump,
                           first_card, second_card, third_card], axis=0)


def main():
    parser = argparse.ArgumentParser(description='Read and convert log files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory for output files')
    parser.add_argument('files', type=str, nargs='+', help='The log files')
    arg = parser.parse_args()

    total_number_of_rounds = 0

    # create output directory
    if not os.path.exists(arg.output_dir):
        print('Creating directory {}'.format(arg.output_dir))
        os.makedirs(arg.output_dir)

    # keep count of the number of output actions generated
    actions = 0

    # parse all files
    for f in arg.files:
        parser = LogParser(f)
        # returns an array of dict with 'players' and 'rounds' as entries
        rounds_players = parser.parse_rounds_and_players()
        total_number_of_rounds += len(rounds_players)

        # open a file for each input file and write it to the output directory
        basename = os.path.basename(f)
        basename, _ = os.path.splitext(basename)
        filename = basename + '.csv'
        filename = os.path.join(arg.output_dir, filename)

        with open(filename, mode='w', newline='') as file:
            print('Processing file: {}'.format(f))
            csv_writer = csv.writer(file)
            for rnd_players in rounds_players:
                # get the player view for making trump
                rnd = rnd_players['round']
                players = rnd_players['players']

                # get a player_rnd for each card played
                player_rnds = PlayerRound.all_from_complete_round(rnd)
                for card_nr, player_rnd in enumerate(player_rnds):
                    features = calculate_features(player_rnd)

                    nr_trick, move_in_trick = divmod(card_nr, 4)
                    # card played (one hot)
                    label = rnd.tricks[nr_trick, move_in_trick]
                    entry = features.tolist()
                    entry.append(label)

                    csv_writer.writerow(entry)
                    actions += 1
                    _print_progress(actions)

    print('Processed {} rounds'.format(total_number_of_rounds))
    print('Processed {} card actions'.format(actions))


def _print_progress(nr_actions):
    if nr_actions % 500 == 0:
        print('.', end='', flush=True)
    if nr_actions % 50000 == 0:
        # new line
        print('')


if __name__ == '__main__':
    main()
