#!/usr/bin/env python3

# BoBoBo

from .conf_parser import token_parser

def get_conf(conf_file):
    with open(conf_file, 'r') as f:
        token_parser.input(f.read_all())
        while True:
            tok = token_parser.token()
            if not tok:
                break
            print(tok)

def read_

class Conf:
