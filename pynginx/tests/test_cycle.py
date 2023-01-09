#!/usr/bin/env python3

# BoBoBo

from pynginx.core.cycle import NgxCycle


def test_one_cycle():
    cycle1 = NgxCycle.instance()
    cycle2 = NgxCycle.instance()

    assert cycle1 is cycle2
