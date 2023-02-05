#!/usr/bin/env python3

# BoBoBo

import threading
import importlib
import json


def engine_func():
    pass


def with_context(context_module_name, context_conf_file):
    print("Build context by %s with %s" %
          (context_module_name, context_conf_file))

    ctx_m = importlib.import_module(context_module_name)
    func = getattr(ctx_m, "build_context")
    ctx = func(context_conf_file)

    if 'logger' in ctx:
        logger = ctx['logger']

    logger.info('build_context is OK!')
    logger.debug('context is %s' % str(ctx))
    return ctx


def route(r, ctx, logger):
    response = {}
    try:
        m, func_name = trans_uri_to_module(r['uri'])
        logger.debug('Route %s to %s.%s' % (r['uri'], m, func_name))
        func_m = importlib.import_module(m)
        func = getattr(func_m, func_name)
        parameters = parse_environ_parameters('GET', r)

        res = func(ctx, **parameters)
        logger.debug('Request: [%s] Result: [%s]' % (str(r), str(res)))
        response['content'] = res
    except Exception:
        logger.error('Failed to route %s' % r, exc_info=True)
    finally:
        return response


def trans_uri_to_module(path):
    mm = path.split('/')
    func_name = mm[-1]
    module_name = '.'.join(mm)

    return module_name[1:], func_name


def parse_environ_parameters(method, environ):
    if method == 'GET':
        return parse_query_string(environ['QUERY_STRING'])
    elif method == 'POST':
        return parse_environ_body(environ)
    else:
        return {}


def parse_query_string(query):
    if not query:
        return {}
    querys = query.split('&')
    querys = list(map(lambda s: s.split('='), querys))
    querys_key = list(map(lambda s: s[0], querys))
    querys_value = list(map(lambda s: s[1], querys))
    return dict(zip(querys_key, querys_value))


def parse_environ_body(environ):
    environ_body_size = int(environ.get('CONTENT_LENGTH', 0))

    if 0 != environ_body_size:
        environ_body = environ['wsgi.input'].read(environ_body_size)
        nd = environ_body.decode('utf-8')
        try:
            parameters = json.loads(nd)
        except json.JSONDecodeError:
            return nd
        else:
            return parameters
    else:
        return {}


def engine_app(wsgi_app):
    """Could be call by engine."""

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
