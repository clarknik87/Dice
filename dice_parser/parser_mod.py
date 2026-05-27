import matplotlib.pyplot as plt
import numpy as np
import math

import dice_parser.dice_distr as dice
from dice_parser.err_codes import *
from dice_parser.lextab import tokens

precedence = (
    ('left','EQUAL_TO','NOT_EQUAL_TO','GREATER_THAN','GREATER_EQUAL','LESS_THAN','LESS_EQUAL'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS')
)

constants: dict[str,float] = {
}

variables: dict[str,float] = {
}

start='statement'

def p_statement_assign(t):
    '''
    statement : NAME EQUALS expression
    '''
    if t[1] in constants:
        raise ConstAssignmentError()
    variables[t[1]] = t[3]
    t[0] = None

def p_statement_expression(t):
    '''
    statement : expression
    '''
    t[0] = t[1]

def p_expression_plus(t):
    '''
    expression : expression PLUS expression
    '''
    t[0] = t[1] + t[3]

def p_expression_minus(t):
    '''
    expression : expression MINUS expression
    '''
    t[0] = t[1] - t[3]

def p_expression_times(t):
    '''
    expression : expression TIMES expression
    '''
    t[0] = t[1] * t[3]

def p_expression_divide(t):
    '''
    expression : expression DIVIDE expression
    '''
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
    if not isinstance(t[3][0], dice.DiceDistribution):
        raise InvalidFunctionArguments(f'{t[3][0]} is not a valid dice formula')
    minimum = t[3][0].minimum()
    maximum = t[3][0].maximum()
    title = ''
    colors = ['b','g','r','c','m','y']
    idx = 0
    for expr in t[3]:
        if isinstance(expr, dice.DiceDistribution):
            title += str(expr)+','
            expr.generate_plot(ax, colors[idx])
            idx += 1
            if expr.minimum() < minimum:
                minimum = expr.minimum()
            if expr.maximum() > maximum:
                maximum = expr.maximum()
        else:
            raise InvalidFunctionArguments(f'{expr} is not a valid dice formula')
    fig.suptitle(title)
    ax.grid(visible=True)
    ax.set_xticks(np.arange(minimum,maximum+1,step=math.ceil((maximum-minimum)/20.0)))
    ax.legend()
    return fig, ax

def p_expression_function(t):
    '''
    expression : NAME LPAREN expressions RPAREN
    '''
    match t[1]:
        case 'roll':
            if len(t[3]) == 1:
                if isinstance(t[3][0], dice.DiceDistribution):
                    t[0] = t[3][0].roll()
                else:
                    raise InvalidFunctionArguments(f'{t[1]}() needs a dice formula')
            else:
                raise InvalidFunctionArguments(f'{t[1]}() needs one argument')
        case 'stats':
            if len(t[3]) == 1:
                if isinstance(t[3][0], dice.DiceDistribution):
                    t[0] = t[3][0].print_stats()
                else:
                    raise InvalidFunctionArguments(f'{t[1]}() function needs a dice formula')
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case 'plot':
            t[0] = plot_dice(t)
        case 'sqrt':
            if len(t[3]) == 1:
                t[0]=math.sqrt(float(t[3][0]))
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case 'ceil':
            if len(t[3]) == 1:
                t[0]=math.ceil(float(t[3][0]))
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case 'round':
            if len(t[3]) == 1:
                t[0]=round(float(t[3][0]))
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case 'floor':
            if len(t[3]) == 1:
                t[0]=math.floor(float(t[3][0]))
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case 'pow':
            if len(t[3]) == 2:
                t[0]=math.pow(int(t[3][0]), int(t[3][1]))
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need two arguments')
        case 'int':
            if len(t[3]) == 1:
                t[0]=int(t[3][0])
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case 'float':
            if len(t[3]) == 1:
                t[0]=float(t[3][0])
            else:
                raise InvalidFunctionArguments(f'{t[1]}() function need one arguments')
        case _:
            raise UndefinedFunctionError(t[1])

def p_expression_dice(t):
    '''
    expression : DICE
    '''
    t[0] = t[1]

def p_comparison_eq(t):
    '''
    expression : expression EQUAL_TO expression
    '''
    t[0] = float(t[1] == t[3])

def p_comparison_ne(t):
    '''
    expression : expression NOT_EQUAL_TO expression
    '''
    t[0] = float(t[1] != t[3])

def p_comparison_gt(t):
    '''
    expression : expression GREATER_THAN expression
    '''
    t[0] = float(t[1] > t[3])

def p_comparison_ge(t):
    '''
    expression : expression GREATER_EQUAL expression
    '''
    t[0] = float(t[1] >= t[3])

def p_comparison_lt(t):
    '''
    expression : expression LESS_THAN expression
    '''
    t[0] = float(t[1] < t[3])

def p_comparison_le(t):
    '''
    expression : expression LESS_EQUAL expression
    '''
    t[0] = float(t[1] <= t[3])

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
    if t[1] in constants:
        t[0] = constants[t[1]]
    elif t[1] in variables:
        t[0] = variables[t[1]]
    else:
        raise VariableKeyError

def p_error(t):
    raise SyntaxError(f'syntax error: {t}') 
