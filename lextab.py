# ------------------------------------------------------------
# lextab.py
# ------------------------------------------------------------
import ply.lex as lex
import math
import DiceDistribution as dice

# List of token names.   This is always required

tokens = (
    'DICE',
    'NAME',
    'NUMBER_DOUBLE',
    'NUMBER_INT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'GREATER_THAN',
    'GREATER_EQUAL',
    'LESS_THAN',
    'LESS_EQUAL',
    'EQUAL_TO',
    'NOT_EQUAL_TO'
)

# Regular expression rules for simple tokens
t_NAME          = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_COMMA         = r','
t_EQUALS        = r'='
t_GREATER_THAN  = r'>'
t_GREATER_EQUAL = r'>='
t_LESS_THAN     = r'<'
t_LESS_EQUAL    = r'<='
t_EQUAL_TO      = r'=='
t_NOT_EQUAL_TO  = r'!='

# A regular expression rule with some action code
def t_DICE(t):
   r'(\d+d\d+)|adv|dis|(max\(\d+d\d+\))|(min\(\d+d\d+\))|(max\(\d+,\d+d\d+\))|(min\(\d+,\d+d\d+\))'
   t.value = dice.DiceDistribution(t.value)
   return t
    
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