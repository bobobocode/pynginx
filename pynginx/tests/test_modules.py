#!/usr/bin/env python3

# BoBoBo

from pynginx.modules import load_modules


def test_load_modules():
    ms = load_modules()
    assert len(ms) == 1
    assert ms[0]
    print(ms[0])
