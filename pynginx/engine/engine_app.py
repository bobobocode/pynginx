#!/usr/bin/env python3

# BoBoBo


import threading


def engine_app(wsgi_app):
    """Wrap wsgi app to engine app.
       And it could be call by engine.
    """

    def app(environ):
        local = threading.local()

        def start_response(status, headers):
            nonlocal local
            if None is headers:
                headers = []
            local.http_response_status = status
            local.http_response_headers = headers

        nonlocal wsgi_app
        res = wsgi_app(environ, start_response)
        response = {}
        response['headers'] = local.http_response_headers
        response['content'] = ''.join([b.decode('utf8') for b in res])
        return response

    return app
