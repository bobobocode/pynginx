#!/usr/bin/env python3

# BoBoBo

from pynginx.modules import pyngx_module_t, pyngx_command_t
from pynginx.modules import PYNGX_HTTP_MODULE
from pynginx.modules import PYNGX_CONF_TAKE1
from pynginx.modules import PYNGX_CONF_TAKE3
from pynginx.modules import PYNGX_HTTP_SRV_CONF
from pynginx.modules import PYNGX_HTTP_LOC_CONF
from . import engine

commands = [pyngx_command_t('with_context',
                            PYNGX_HTTP_SRV_CONF | PYNGX_CONF_TAKE3,
                            engine.with_context,
                            None
                            ),
            pyngx_command_t('engine_func',
                            PYNGX_HTTP_LOC_CONF | PYNGX_CONF_TAKE1,
                            engine.engine_func,
                            None
                            ),
            pyngx_command_t('engine_app',
                            PYNGX_HTTP_LOC_CONF | PYNGX_CONF_TAKE3,
                            engine.engine_app,
                            None)]

"""Define Engine module"""
module = pyngx_module_t('engine', commands, PYNGX_HTTP_MODULE, None)
