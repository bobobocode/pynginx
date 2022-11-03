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

    ngx_cycle = NgxCycle.instance().init_cycle(options.conf_file)

    # Main loop
        # Event module
        # TCP Connection
        # Follow conf file
        # HTTP framework
            # HTTP module
                # HTTP filter module
            # HTTP other module


if __name__ == "__main__":
    main()
