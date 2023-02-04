#!/usr/bin/env python3

# BoBoBo

import pynginx.cycle as cycle


def test_init_cycle():
    init_cycle = cycle.PyNgxCycle()
    init_cycle.conf_file = '../../examples/conf/nginx.conf'
    pyngx_cycle = cycle.pyngx_init_cycle(init_cycle)

    assert pyngx_cycle
    assert pyngx_cycle != init_cycle
