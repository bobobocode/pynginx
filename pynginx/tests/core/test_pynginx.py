#!/usr/bin/env python3

# BoBoBo

import pynginx.core.pynginx as pynginx


def test_pynginx():
    args = ['pynginx',
            '-c',
            'conf/nginx.conf'
            ]

    options = pynginx.get_options(args)

    assert options.conf_file == 'conf/nginx.conf'
