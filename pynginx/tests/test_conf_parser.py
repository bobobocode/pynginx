#!/usr/bin/env python3

# BoBoBo

from pynginx.conf.conf_parser import token_parser


def test_token_parser():
    conf_str = """
        events {}

        master_process off;

        error_log /usr/local/nginx/logs/debug.log debug;

        http {
            server {
                listen       8080;
                server_name  localhost;
                with_context /usr/local/app/engine_func context /usr/local/app/engine_func/conf.yaml;

                location /func {
                    engine_func  /usr/local/app/engine_func;
                }

                location /app {
                    engine_app /usr/local/app/engine_app helloworld app;
                }
            }
        }
    """
    token_parser.input(conf_str)
    while True:
        tok = token_parser.token()
        if not tok:
            break
        print(tok)
