#!/usr/bin/env python3

# BoBoBo

import logging
import socket
import select
from .buffer import HttpRequestBuffer
from .. import cycle


def bootstrap(pyngx_cycle):
    host, port = cycle.get_server_address(pyngx_cycle)
    logger = cycle.get_error_logger(pyngx_cycle)
    httpd = EngineServer(host, port, logger,
                         cycle.get_router(pyngx_cycle),
                         cycle.get_context(pyngx_cycle))
    httpd.serve_forever()


class EngineServer:

    def __init__(self, host, port, router, context, logger=None):
        self.host = host
        self.port = port
        if not logger:
            logger = self.default_logger()
        self.logger = logger

        self.router = router
        self.context = context

        self.connects = {}
        self.responses = {}
        self.responses_pathes = {}
        self.request_package_buffer = HttpRequestBuffer()

    def serve_forever(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.logger.info('PyNginx started listening')
        self.logger.info('...host: %s' % self.host)
        self.logger.info('...port: %s' % self.port)

        try:
            self.epoll = select.epoll()
            self.epoll.register(self.server_socket.fileno(),
                                select.EPOLLIN | select.EPOLLET)
        except:
            self.epoll = select.poll()
            self.epoll.register(self.server_socket.fileno(),
                                select.POLLIN | select.POLLERR)

        self.logger.info('registered server socket')
        self.logger.info('start event loop...')
        try:
            while True:
                epoll_list = self.epoll.poll()
                for fd, event in epoll_list:
                    if fd == self.server_socket.fileno():
                        new_socket, new_addr = self.server_socket.accept()
                        self.logger.debug('accept %s' % str(new_addr))
                        try:
                            self.epoll.register(new_socket.fileno(),
                                                select.EPOLLIN | select.EPOLLET)
                        except:
                            self.epoll.register(new_socket.fileno(),
                                                select.POLLIN | select.POLLERR)
                        self.connects[new_socket.fileno()] = new_socket
                    elif event == select.POLLIN or event == select.POLLERR:
                        if fd in self.connects:
                            self.logger.debug(
                                'epoll event: socket fd[%s] readable' % fd)
                            self.process_socket_in(fd)
                        elif fd in self.responses:
                            self.logger.debug(
                                'epoll event: named pipe fd[%s] readable' % fd)
                            self.process_socket_out(fd)
                        else:
                            self.logger.error(
                                'unknown epoll event: fd[%s] event[%s]' % (fd, event))
                    elif event & select.EPOLLHUP:
                        if fd in self.connects:
                            self.logger.debug(
                                'close socket fd[%s] for EPOLLHUP' % fd)
                            self.epoll.unregister(fd)
                            self.connects[fd].close()
                            del self.connects[fd]
                            self.request_package_buffer.clear_fd(fd)
        finally:
            self.epoll.unregister(self.server_socket.fileno())
            self.epoll.close()
            self.server_socket.close()

    def process_socket_in(self, fd):
        request_bytes = self.connects[fd].recv(1024)
        if not request_bytes:
            return

        self.logger.debug(
            'read %s bytes from fd[%s]' % (len(request_bytes), fd))
        self.request_package_buffer.append(fd, request_bytes)
        environ = self.request_package_buffer.next_package(fd)
        if environ:
            # TODO: execute filters here
            try:
                response = self.do_wsgi_request(environ, fd)
            except Exception:
                self.logger.error(
                    'fd[%s] failed request: %s' % (fd, str(environ)),
                    exc_info=True)
                self.response_error(fd, 500)
            else:
                if response:
                    self.logger.debug('response content: %s' % str(response))
                    for s in response:
                        if s:
                            self.connects[fd].send(s)

    def make_start_response(self, fd):
        socket = self.connects[fd]

        def start_response(status, headers):
            nonlocal socket
            self.logger.debug('response status %s' % status)
            socket.send(('HTTP/1.1 ' + status + '\r\n').encode('utf-8'))
            for t in headers:
                self.logger.debug('response header %s:%s' % tuple(t))
                socket.send((t[0] + ':' + t[1] + '\r\n').encode('utf-8'))
            socket.send('\r\n'.encode('utf-8'))

        return start_response

    def response_error(self, fd, error_code):
        if error_code == 404:
            resp = self.response_404()
        else:
            resp = self.response_500()
        start_response = self.make_start_response(fd)
        start_response(resp['status'], resp['headers'])

    def do_wsgi_request(self, environ, fd):
        self.logger.debug('do request from fd[%s]: %s' % (fd, environ))
        return self.router(environ['PATH_INFO'])(self.context,
                                                 environ, self.make_start_response(fd))

    def response_400(self):
        return {'headers': [
            ('Content-Type', 'text/html;charset=utf-8'),
            ('Content-Length', '0')],
            'status': '400 Bad Request',
            'content': ''}

    def response_500(self):
        return {'headers': [
            ('Content-Type', 'text/html;charset=utf-8'),
            ('Content-Length', '0')],
            'status': '500 Internal Server Error',
            'content': ''}

    def default_logger(self):
        level = logging.DEBUG
        log_file = 'pynginx.log'
        logger_name = 'pynginx-default-log'

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
