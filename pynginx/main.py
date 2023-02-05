#!/usr/bin/env python3

# BoBoBo

from argparse import ArgumentParser
from . import modules
from . import cycle
from .server import server


def pyngx_get_options(args=None):
    if args is None:
        import sys
        args = sys.argv

    parser = ArgumentParser(prog=args[0],
                            usage='pynginx.py -c <nginx conf file>')
    parser.add_argument("-c", dest="conf_file",
                        help="nginx conf file path",
                        default=None)

    return parser.parse_args(args[1:])


def main():
    opts = pyngx_get_options()
    print('PyNginx starting...')
    print(f'conf_file: {opts.conf_file}')
    ms = modules.load_modules()
    print('modules: ' + str([m.name for m in ms]))

    init_cycle = cycle.PyNgxCycle()
    init_cycle.conf_file = opts.conf_file
    init_cycle.modules = ms

    pyngx_cycle = cycle.pyngx_init_cycle(init_cycle)

    # Let`s start from an available web server first
    server.bootstrap(pyngx_cycle)
