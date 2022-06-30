# ------------------------------------------------------------
# lextab.py
# ------------------------------------------------------------
import ply.lex as lex
import dice
import math

# List of token names.   This is always required
# tokens = (
    # 'DICE',
    # 'NAME',
    # 'NUMBER_DOUBLE',
    # 'NUMBER_INT',
    # 'PLUS',
    # 'MINUS',
    # 'TIMES',
    # 'DIVIDE',
    # 'LPAREN',
    # 'RPAREN',
# )

tokens = (
    'NAME',
    'NUMBER_DOUBLE',
    'NUMBER_INT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'COLON',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON   = r','
t_EQUALS  = r'='

# A regular expression rule with some action code
#def t_DICE(t):
#    r'\d+d\d+'
#    t.value = dice.Dice(t.value)
#    return t
    
def t_NUMBER_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)    
    return t

def t_NUMBER_INT(t):
    r'\d+'
    t.value = float(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)