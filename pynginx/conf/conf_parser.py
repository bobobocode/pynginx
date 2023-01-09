#!/usr/bin/env python3

# BoBoBo

import ply.lex as lex

tokens = ['NUMBER',
          'LBRACE',
          'RBRACE',
          'SEMICOLON',
          'ID'
          ]

reserved = {'events' : 'EVENTS',
            'error_log' : 'ERROR_LOG',
            'http' : 'HTTP',
            'server' : 'SERVER',
            'listen' : 'LISTEN',
            'with_context' : 'WITH_CONTEXT',
            'location' : 'LOCATION',
            }

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'

tokens = tokens + list(reserved.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


parser = lex.lex()
