#!/bin/python3
import argparse
import os
from sys import argv


version = '0.1'


def main():
    # create parser
    parser = argparse.ArgumentParser(description="A simple program that"
                                                 " replaces the original "
                                                 "pixels of a picture with other things")

    # add arguments
    parser.add_argument('--version', '-V', action='version', version='version: {}'.format(version))
    parser.add_argument('command', metavar='command',
                        type=str,
                        help='choose one command: '
                             '1. fii: fill image with image '
                             '2. fit: fill image with text')

    # parse

    args = parser.parse_args(argv[1:2]) # python3 fiot.py arguments
    if argv[0] == './' + __file__:
        args = parser.parse_args([__file__].append(argv[1:2])) # ./fiot.py arguments

    # use sub command to parse
    command = args.command
    subcommand = 'python3 ' + argv[1] + '.py ' + ' '.join(argv[2:])
    if command == 'fii':
        os.system(subcommand)
    elif command == 'fit':
        os.system(subcommand)


if __name__ == '__main__':
    main()
