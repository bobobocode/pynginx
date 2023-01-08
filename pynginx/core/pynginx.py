#!/usr/bin/env python3

# BoBoBo

import sys
from argparse import ArgumentParser


def get_options(args):
    if args is None: args = sys.argv

    parser = ArgumentParser(prog=args[0], usage='pynginx.py \
            -c <nginx conf file>')

    parser.add_argument("-c", dest="conf_file",
                        help="nginx conf file path", default=None)

    return parser.parse_args(args[1:])


def main():
    options = get_options()


if __name__ == "__main__":
    main()
