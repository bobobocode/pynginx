#!/usr/bin/env python3

# BoBoBo

import copy
from .conf import ngxconf


class PyNgxCycle:
    """Single instance for every process

    Attributes:
        options: command line options
        conf_ctx: conf_file parsed
    """

    def __init__(self):
        pass

    def copy(self):
        return copy.deepcopy(self)


def pyngx_init_cycle(init_cycle):
    """TODO: Fix the gap here
    """

    cf = ngxconf.PyNgxConf()
    conf_ctx = ngxconf.pyngx_conf_parse(cf, init_cycle.conf_file)

    new_pyngx_cycle = init_cycle.copy()
    new_pyngx_cycle.conf_ctx = conf_ctx

    return new_pyngx_cycle


def get_server_address(pyngx_cycle):
    return '', 8080


def get_error_logger(pyngx_cycle):
    import logging

    level = logging.DEBUG
    log_file = 'default-pynginx.log'
    logger_name = 'default-pynginx-logger'

    form = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(form)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


def get_router(pyngx_cycle):
    def router(path_info):
        def _do(context, environ, start_response):
            start_response(200, None)
            return 'Not ready yet'
        return _do
    return router


def get_context(pyngx_cycle):
    return None
