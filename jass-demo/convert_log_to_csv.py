# HSLU
#
# Created by Thomas Koller on 10.09.18
#


import os
import csv
import argparse

from jass.base.const import PUSH
from jass.base.player_round import PlayerRound
from jass.io.log_parser import LogParser


def main():
    parser = argparse.ArgumentParser(description='Read and convert log files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory for output files')
    parser.add_argument('files', type=str, nargs='+', help='The log files')
    arg = parser.parse_args()

    total_number_of_rounds = 0

    if not os.path.exists(arg.output_dir):
        print('Creating directory {}'.format(arg.output_dir))
        os.makedirs(arg.output_dir)

    actions = 0
    for f in arg.files:
        parser = LogParser(f)
        rounds = parser.parse_rounds()
        total_number_of_rounds += len(rounds)

        # open a file for each input file and write it to the output directory
        basename = os.path.basename(f)
        basename, _ = os.path.splitext(basename)
        filename = basename + '.csv'
        filename = os.path.join(arg.output_dir, filename)

        with open(filename, mode='w', newline='') as file:
            print('Processing file: {}'.format(f))
            csv_writer = csv.writer(file)
            for rnd in rounds:
                # get the player view for making trump
                if not rnd.forehand:
                    # was not declared forehand, so add a entry for push
                    player_rnd = PlayerRound.trump_from_complete_round(rnd, forehand=True)
                    entry = player_rnd.hand.tolist()
                    # add a boolean (1) for forehand
                    entry.append(1)
                    entry.append(PUSH)
                    csv_writer.writerow(entry)
                    actions += 1
                    _print_progress(actions)

                    # and then the entry for backhand
                    player_rnd = PlayerRound.trump_from_complete_round(rnd, forehand=False)
                    entry = player_rnd.hand.tolist()
                    # add a boolean (0) for rearhand
                    entry.append(0)
                    entry.append(rnd.trump)
                    csv_writer.writerow(entry)
                    actions += 1
                    _print_progress(actions)
                else:
                    # add only one entry for forehand
                    player_rnd = PlayerRound.trump_from_complete_round(rnd, forehand=True)
                    entry = player_rnd.hand.tolist()
                    # add a boolean (0) for rearhand
                    entry.append(1)
                    entry.append(rnd.trump)
                    csv_writer.writerow(entry)
                    actions += 1
                    _print_progress(actions)

    print('Processed {} rounds'.format(total_number_of_rounds))
    print('Processed {} trump actions'.format(actions))


def _print_progress(nr_actions):
    if nr_actions % 100 == 0:
        print('.', end='', flush=True)
    if nr_actions % 1000 == 0:
        # new line
        print('')


if __name__ == '__main__':
    main()

#{"rounds":[{"trump":0,"dealer":3,"tss":1,"tricks":[{"cards":["D10","D8","DJ","DA"],"points":41,"win":0,"first":2},{"cards":["S9","S10","D6","SA"],"points":21,"win":2,"first":0},{"cards":["CA","C7","C10","CJ"],"points":23,"win":2,"first":2},{"cards":["HA","H6","C6","H7"],"points":11,"win":2,"first":2},{"cards":["SQ","C8","SK","S6"],"points":7,"win":0,"first":2},{"cards":["DK","H10","H8","H9"],"points":14,"win":0,"first":0},{"cards":["DQ","HJ","S7","CQ"],"points":8,"win":0,"first":0},{"cards":["D9","S8","C9","CK"],"points":18,"win":0,"first":0},{"cards":["D7","SJ","HQ","HK"],"points":14,"win":0,"first":0}],"player":[{"hand":[]},{"hand":[]},{"hand":[]},{"hand":[]}],"jassTyp":"SCHIEBER_2500"},{"trump":1,"dealer":2,"tss":1,"tricks":[{"cards":["HA","H6","H9","H8"],"points":25,"win":3,"first":1},{"cards":["C10","S10","HQ","HK"],"points":27,"win":0,"first":3},{"cards":["CQ","C8","D10","CK"],"points":17,"win":1,"first":0},{"cards":["C9","CA","D8","DQ"],"points":14,"win":0,"first":1},{"cards":["CJ","D9","S7","C7"],"points":2,"win":0,"first":0},{"cards":