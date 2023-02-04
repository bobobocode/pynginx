#!/usr/bin/env python3

# BoBoBo

from collections import namedtuple
from .token_parser import parser as token_parser


NGX_CONF_OK = None
NGX_CONF_ERROR = -1
NGX_CONF_BLOCK_START = 1
NGX_CONF_BLOCK_DONE = 2
NGX_CONF_FILE_DONE = 3


class PyNgxConf:
    conf_file = None
    args = []


pyngx_conf_t = namedtuple('pyngx_conf_t',
                          ['conf_file', 'ctx', 'py_content', 'args'])


def gen_pyngx_conf_read_token(cf):
    conf_file = cf.conf_file
    with open(conf_file, mode='r') as f:
        token_parser.input(f.read())
        while True:
            tok = token_parser.token()
            if not tok:
                return NGX_CONF_FILE_DONE

            if tok.type == 'ID' or tok.type == 'VALUE':
                cf.args.append(tok.value)
                continue

            elif tok.type == 'LBRACE':
                yield NGX_CONF_BLOCK_START

            elif tok.type == 'RBRACE':
                yield NGX_CONF_BLOCK_DONE

            elif tok.type == 'SEMICOLON':
                directive = cf.args[0]
                values = cf.args[1:]
                cf.ctx[directive] = values
                yield NGX_CONF_OK


def pyngx_conf_handler(cf):
    pass


def pyngx_conf_parse(cf, conf_file):
    cf.conf_file = conf_file
    pyngx_conf_read_token = gen_pyngx_conf_read_token(cf)
    conf_ctx = {}
    cf.ctx = conf_ctx
    for rc in pyngx_conf_read_token:
        if rc == NGX_CONF_OK:
            pyngx_conf_handler(cf)

        elif rc == NGX_CONF_BLOCK_START:
            continue

        elif rc == NGX_CONF_BLOCK_DONE:
            continue

        elif rc == NGX_CONF_FILE_DONE:
            return conf_ctx

        else:  # This should not happen
            return None
