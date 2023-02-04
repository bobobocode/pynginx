#!/usr/bin/env python3

# BoBoBo

from collections import namedtuple
import importlib

PYNGX_HTTP_MODULE = 0x50545448  # "HTTP"

PYNGX_CONF_TAKE1 = 0x00000002
PYNGX_CONF_TAKE2 = 0x00000004
PYNGX_CONF_TAKE3 = 0x00000008

PYNGX_HTTP_MAIN_CONF = 0x02000000
PYNGX_HTTP_SRV_CONF = 0x04000000
PYNGX_HTTP_LOC_CONF = 0x08000000


pyngx_module_t = namedtuple('pyngx_module_t',
                            ['name', 'commands', 'type', 'init_module'])

pyngx_command_t = namedtuple('pyngx_command_t',
                             ['name', 'type', 'set', 'conf'])

HTTP_MODULES = ('pynginx.engine',)


def load_modules():
    """Like nginx compile modules
    """
    global HTTP_MODULES

    mms = []
    for m_name in HTTP_MODULES:
        m = importlib.import_module(m_name)
        mms.append(m.module)

    return mms
