#!/usr/bin/env python3

# BoBoBo

from pynginx.conf.token_parser import parser as token_parser
from pynginx.conf.ngxconf import pyngx_conf_t
from pynginx.conf.ngxconf import gen_ngx_conf_read_token


test_conf_file = '../../examples/conf/nginx.conf'


def test_token_parser():
    """Test no exceptions
    """
    with open(test_conf_file, mode='r') as f:
        token_parser.input(f.read())
        while True:
            tok = token_parser.token()
            if not tok:
                break
            print(tok)


def test_ngx_conf_read_token():
    cf = pyngx_conf_t(test_conf_file, None, None, [])
    ngx_conf_read_token = gen_ngx_conf_read_token(cf)
    for rc in ngx_conf_read_token:
        print(rc)
        print(cf.args)
        cf.args.clear()
