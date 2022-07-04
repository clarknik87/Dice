import ply.lex as lex
import ply.yacc as yacc
import matplotlib.pyplot as plt
import numpy as np
import math
import lextab
import os

import DiceDistribution as dice

# Get the token map from the lexer.
from lextab import tokens

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
)

variables = {
    'pi': math.pi,
    'e': math.e,
}

start='statement'

def p_statement_assign(t):
    '''
    statement : NAME EQUALS expression
    '''
    variables[t[1]] = t[3]

def p_statement_expression(t):
    '''
    statement : expression
    '''
    if isinstance(t[1], dice.DiceDistribution):
        print(t[1].roll())
    elif t[1] != None:
        print(t[1])

def p_expression_binop(t):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression DIVIDE expression
               | expression TIMES expression
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]

def p_expression_uminus(t):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    t[0] = -t[2]

def p_expression_group(t):
    '''
    expression : LPAREN expression RPAREN
    '''
    t[0] = t[2]

def p_expressions(t):
    '''
    expressions : expressions COMMA expression
               | expression
               |
    '''
    if len(t) == 0:
        t[0]=None
        return
    t[0] = [t[1]] if len(t) == 2 else t[1] + [t[3]]

def plot_dice(t):
    fig, ax = plt.subplots()
    minimum = t[3][0].minimum()
    maximum = t[3][0].maximum()
    title = ''
    colors = ['b','g','r','c','m','y']
    idx = 0
    for expr in t[3]:
        if isinstance(expr, dice.DiceDistribution):
            print(expr)
            title += str(expr)+','
            expr.print_stats()
            expr.generate_plot(ax, colors[idx])
            idx += 1
            if expr.minimum() < minimum:
                minimum = expr.minimum()
            if expr.maximum() > maximum:
                maximum = expr.maximum()
        else:
            print('%s() function needs a dice formula' % t[1])
    plt.title(title)
    plt.grid()
    plt.xticks(np.arange(minimum,maximum+1,step=math.ceil((maximum-minimum)/20.0)))
    plt.legend()
    plt.show()
    t[0]=None

def p_expression_function(t):
    '''
    expression : NAME LPAREN expressions RPAREN
    '''

    if t[1] == 'stats':
        if len(t[3]) == 1:
            if isinstance(t[3][0], dice.DiceDistribution):
                t[3][0].print_stats()
                t[0]=None
            else:
                print('%s() function needs a dice formula' % t[1])
        else:
           print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'plot':
        plot_dice(t)
        return

    if t[1] == 'sqrt':
        if len(t[3]) == 1:
            t[0]=math.sqrt(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'ceil':
        if len(t[3]) == 1:
            t[0]=math.ceil(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'round':
        if len(t[3]) == 1:
            t[0]=round(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'floor':
        if len(t[3]) == 1:
            t[0]=math.floor(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'pow':
        if len(t[3]) == 2:
            t[0]=math.pow(int(t[3][0]), int(t[3][1]))
        else:
            print('%s() function need two arguments' % t[1])
        return
    elif t[1] == 'int':
        if len(t[3]) == 1:
            t[0]=int(t[3][0])
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'float':
        if len(t[3]) == 1:
            t[0]=float(t[3][0])
        else:
            print('%s() function need one arguments' % t[1])
        return
    print('Undefined function \'%s\'' % t[1])
    t[0] = None

def p_expression_dice(t):
    '''
    expression : DICE
    '''
    t[0] = t[1]

def p_expression_number(t):
    '''
    expression : NUMBER_INT
               | NUMBER_DOUBLE
    '''
    t[0] = t[1]

def p_expression_name(t):
    '''
    expression : NAME
    '''
    try:
        t[0] = variables[t[1]]
    except LookupError:
        print('Undefined name \'%s\'' % t[1])
        t[0] = None

def p_error(t):
    print('Syntax error at \'%s\'' % t.value)

def main():
    lexer = lex.lex(module=lextab)
    parser = yacc.yacc()
    while True:
        expr = input('>> ')
        if "clear" in expr:
                os.system('cls')
        elif 'quit' in expr:
            return
        elif expr != '':
            result = parser.parse(expr)

if __name__ == "__main__":
    main()