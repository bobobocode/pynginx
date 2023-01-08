#!/usr/bin/env python3

# BoBoBo

import os
import socket
import select
import json
import driven.util as util
from .buffer import HttpRequestBuffer


class EpollHttpServer:

    def __init__(self, host, port, log_conf, apps,
                 driven_process=None):
        self.host = host
        self.port = port
        self.logger = util.get_logger(log_conf)

        self.apps = apps
        if driven_process:
            self.do_request_mode = 'driven'
            self.driven_process = driven_process
        else:
            self.do_request_mode = 'wsgi'

        self.connects = {}
        self.responses = {}
        self.responses_pathes = {}
        self.request_package_buffer = HttpRequestBuffer()
        self.logger.info(
            'sengine server inited with process mode: %s' % self.do_request_mode)
        self.logger.info('...host: %s' % self.host)
        self.logger.info('...port: %s' % self.port)

    def serve_forever(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.logger.info('started listening')

        self.epoll = select.epoll()
        self.epoll.register(self.server_socket.fileno(),
                            select.EPOLLIN | select.EPOLLET)
        self.logger.info('registered server socket')

        self.logger.info('start epoll processing loop...')
        try:
            while True:
                epoll_list = self.epoll.poll()
                for fd, event in epoll_list:
                    if fd == self.server_socket.fileno():
                        new_socket, new_addr = self.server_socket.accept()
                        self.logger.debug('accept %s' % str(new_addr))
                        self.epoll.register(new_socket.fileno(),
                                            select.EPOLLIN | select.EPOLLET)
                        self.connects[new_socket.fileno()] = new_socket
                    elif event == select.EPOLLIN or event == select.EPOLLET:
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
            except Exception as ex:
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

    def process_socket_out(self, named_pipe_fd):
        response_bytes, fd = self.read_from_named_pipe(named_pipe_fd)
        if response_bytes:
            response_str = response_bytes.decode('utf-8')
            self.logger.debug('read from named pipe fd[%s]: %s' % (
                named_pipe_fd, response_str))
            # driven-app should return json response with app_response
            try:
                response_json = json.loads(response_str)
                self.response_driven_app(fd, response_json)
            except Exception as ex:
                self.logger.error(
                    'fd[%s] failed to response app result: %s'
                    % (fd, response_str),
                    exc_info=True)
                self.response_error(fd, 500)
        else:
            self.logger.error(
                'read from named pipe fd[%s] none' % named_pipe_fd)
            self.response_error(fd, 500)

    def read_from_named_pipe(self, named_pipe_fd):
        if named_pipe_fd:
            s = bytes()
            while True:
                s += os.read(named_pipe_fd, 1024)
                self.logger.debug(
                    'read %s bytes from named pipe fd[%s]'
                    % (len(s), named_pipe_fd))
                if s.endswith(b'\r\n'):
                    break

            self.logger.debug(
                'close named pipe fd[%s] after read' % named_pipe_fd)
            self.epoll.unregister(named_pipe_fd)
            os.close(named_pipe_fd)
            os.remove(self.responses_pathes[named_pipe_fd])
            socket_fd = self.responses[named_pipe_fd]
            del self.responses[named_pipe_fd]
            del self.responses_pathes[named_pipe_fd]

            return s, socket_fd
        else:
            return None

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
            resp = app_response.response_404()
        else:
            resp = app_response.response_500()
        start_response = self.make_start_response(fd)
        start_response(resp['status'], resp['headers'])

    def response_driven_app(self, fd, resp):
        if resp:
            # TODO: execute filters here
            start_response = self.make_start_response(fd)
            start_response(resp['status'], resp['headers'])
            self.connects[fd].send(resp['content'].encode('utf-8'))
        else:
            response_error(self, fd)

    def do_wsgi_request(self, environ, fd):
        '''
        top path decides with app to call
        '''
        self.logger.debug('do request from fd[%s]: %s' % (fd, environ))
        if self.do_request_mode == 'wsgi':
            request_app_name = environ['PATH_INFO'].split('/')[1]
            if request_app_name in self.apps:
                return self.apps[request_app_name](environ,
                                                   self.make_start_response(fd))
            else:
                return self.response_error(fd, 404)
        elif self.do_request_mode == 'driven':
            try:
                response_named_pipe = driven_process.apply_response_pipe()
                response_fd = os.open(response_named_pipe,
                                      os.O_RDONLY | os.O_NONBLOCK)
                self.epoll.register(
                    response_fd, select.EPOLLIN | select.EPOLLET)
            except Exception as ex:
                self.logger.error(
                    'failed to register epoll with response named pipe fd[%s]'
                    % response_fd, exc_info=True)
                return self.response_error(fd, 500)
            self.responses[response_fd] = fd
            self.responses_pathes[response_fd] = response_named_pipe
            self.logger.debug('register named pipe fd[%s]' %
                              response_fd)

            try:
                driven_process.driven_process_wsgi_request(
                    environ, response_named_pipe)
            except Exception as ex:
                self.logger.error(
                    'failed to do wsgi request using driven process',
                    exc_info=True)
                return self.response_error(fd, 500)

            return None
        else:
            raise Exception('ERROR: sengine server mode')
