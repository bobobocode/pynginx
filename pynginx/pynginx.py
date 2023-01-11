#!/usr/bin/env python3

# BoBoBo

import sys
from os import path
sys.path.append(path.dirname(path.abspath(__file__)))

from argparse import ArgumentParser
from cycle import PyNginxCycle
import conf.conf as conf


def get_options(args=None):
    if args is None: args = sys.argv

    parser = ArgumentParser(prog=args[0], usage='pynginx.py \
            -c <nginx conf file>')

    parser.add_argument("-c", dest="conf_file",
                        help="nginx conf file path", default=None)

    return parser.parse_args(args[1:])


def main():
    pyngx_cycle = PyNginxCycle()

    options = get_options()
    pyngx_cycle.options = options

    conf_ctx = conf.get_conf_ctx(pyngx_cycle)
    pyngx_cycle.conf_ctx = conf_ctx


if __name__ == "__main__":
    main()
