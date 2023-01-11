#!/usr/bin/env python3

# BoBoBo

from .conf_parser import token_parser

def get_conf_ctx(pyngx_cycle):
    conf_file = pyngx_cycle.options.conf_file

    with open(conf_file, mode = 'r') as f:
        token_parser.input(f.read())
        while True:
            tok = token_parser.token()
            if not tok:
                break
            print(tok)
