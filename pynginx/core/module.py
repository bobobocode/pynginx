#!/usr/bin/env python3

# BoBoBo

from pynginx.core.core import ngx_core_module
from pynginx.core.log import ngx_errlog_module
from pynginx.core.conf import ngx_conf_module

ngx_modules = [ngx_core_module,
               ngx_errlog_module,
               ngx_conf_module]
