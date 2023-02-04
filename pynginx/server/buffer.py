#!/usr/bin/env python3

# BoBoBo

from collections import defaultdict
from . import util


class HttpRequestBuffer:

    def __init__(self):
        self.fds = defaultdict(dict)

    def clear_fd(self, fd):
        if fd in self.fds:
            del self.fds[fd]

    def append(self, fd, request_bytes):
        if self.fds[fd].get('bytes', None) is None:
            self.fds[fd]['bytes'] = bytearray()
            self.fds[fd]['read_index'] = 0
        self.fds[fd]['bytes'] += request_bytes

    def next_package(self, fd):
        # Read and parse first line as dict
        # If had read before, pass
        # If not valid http request line, discard
        # If no valid http request line, return None
        if not self.fds[fd].get('request_line', None):
            request_line = self.parse_http_request_line(fd)
            if request_line is None:
                return None
            self.fds[fd]['request_line'] = request_line

        # Read until CRLF
        # If had read before, pass
        # If no CRLF, return None
        if not self.fds[fd].get('headers', None):
            headers = self.parse_http_headers(fd)
            if headers is None:
                return None
            self.fds[fd]['headers'] = headers

        # If length is 0, return ''
        # If not enough bytes, return None
        body = self.read_http_body(fd,
                                   int(headers.get('Content-Length', 0)))
        if body is None:
            return None
        self.fds[fd]['body'] = body

        wsgi_request = self.setup_wsgi_request(self.fds[fd])
        self.clear_already_read(fd)
        return wsgi_request

    def get_bytes(self, fd):
        try:
            return self.fds[fd]['bytes']
        except KeyError:
            return None

    def read_line(self, fd):
        fd_buffer = self.fds.get(fd, None)
        if fd_buffer is None:
            return None

        buffer_bytes = fd_buffer['bytes']
        if not buffer_bytes:
            return None

        line_index = buffer_bytes.find(b'\r\n', fd_buffer['read_index'])
        if line_index < 0:
            return None

        # Pop the line
        line = buffer_bytes[fd_buffer['read_index']:line_index]
        fd_buffer['read_index'] += len(line) + 2
        return line.decode('utf-8')

    def clear_read(self, fd):
        fd_buffer = self.fds[fd]
        read_index = fd_buffer['read_index']
        del fd_buffer['bytes'][:read_index]
        fd_buffer['read_index'] = 0

    def parse_http_request_line(self, fd):
        while True:
            line = self.read_line(fd)
            if line is None:
                return None
            self.clear_already_read(fd)
            request_line = util.parse_http_request_line(line)
            if request_line:
                return request_line

    def give_back(self, fd):
        fd_buffer = self.fds[fd]
        fd_buffer['read_index'] = 0

    def parse_http_headers(self, fd):
        headers = {}
        while True:
            line = self.read_line(fd)
            if line is None:
                self.give_back(fd)
                return None
            if line == '':
                break
            h = line.split(':')
            if len(h) != 2:  # Invalid header content
                continue
            else:
                headers[h[0].strip()] = h[1].strip()
        self.clear_read(fd)
        return headers

    def read_http_body(self, fd, length):
        buffer_bytes = self.fds[fd]['bytes']
        body = buffer_bytes[:length].decode('utf-8')
        self.fds[fd]['read_index'] += len(body)
        self.clear_read(fd)
        return body

    def setup_wsgi_request(self, fd_buffer):
        request_line = fd_buffer['request_line']
        headers = fd_buffer['headers']
        body = fd_buffer['body']

        pathes = [request_line['PATH_INFO'], request_line['QUERY_STRING']]
        environ = util.convert_wsgi_request(
            request_line['REQUEST_METHOD'], pathes, headers, body)
        return environ

    def clear_already_read(self, fd):
        fd_buffer = self.fds[fd]
        fd_buffer['request_line'] = None
        fd_buffer['headers'] = None
        fd_buffer['body'] = None
