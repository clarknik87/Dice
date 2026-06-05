import ply.lex as lex
import ply.yacc as yacc
from dice_parser import lextab, parser_mod
from dice_parser.dice_distr import DiceDistribution, DiceStats
from dice_parser.err_codes import *
from dice_parser.var_graph import var_graph, KeyRedefinitionError, VariableKeyError
from enum import Enum, auto
from matplotlib.axes import Axes
from matplotlib.figure import Figure

class ParseError(Enum):
    ERR_CONST_ASSIGNMENT = auto()
    ERR_NAME_NOT_FOUND = auto()
    ERR_ZERO_DIVISION = auto()
    ERR_TYPE_UNSUPPORTED = auto()
    ERR_UNDEFINED_FUNC = auto()
    ERR_INVALID_FUNC_ARG = auto()
    ERR_SYNTAX_ERROR = auto()
    ERR_UNKNOWN_OUTPUT = auto()

class DiceParser:
    def __init__(self, constants:dict[str,str] = {}, variables:dict[str,str] = {}) -> None:
        self.lexer = lex.lex(module=lextab)
        self.parser = yacc.yacc(module=parser_mod)
        self.parser.variables = var_graph(self.lexer, self.parser)
        self.parser.variables.init_variables(variables, constants)

    def parse(self, expr:str) -> int|float|DiceDistribution|DiceStats|tuple[Figure,Axes]|ParseError|None:
        if expr.strip() == '':
            return None
        try:
            val = self.parser.parse(expr)
            if isinstance(val, (int,float,DiceDistribution,DiceStats)):
                return val
            elif isinstance(val, tuple) and list(map(type, val)) == [Figure, Axes]:
                return val
            elif val is None:
                return None
            else:
                return ParseError.ERR_UNKNOWN_OUTPUT
        except KeyRedefinitionError:
            return ParseError.ERR_CONST_ASSIGNMENT
        except ZeroDivisionError:
            return ParseError.ERR_ZERO_DIVISION
        except TypeError:
            return ParseError.ERR_TYPE_UNSUPPORTED
        except VariableKeyError:
            return ParseError.ERR_NAME_NOT_FOUND
        except UndefinedFunctionError:
            return ParseError.ERR_UNDEFINED_FUNC
        except InvalidFunctionArguments:
            return ParseError.ERR_INVALID_FUNC_ARG
        except SyntaxError:
            return ParseError.ERR_SYNTAX_ERROR

    def interpolate(self, expr:str) -> str:
        while ((sidx := expr.find('{')) != -1) and ((eidx := expr.find('}')) != -1):
            parse_result = self.parse(expr[sidx+1:eidx])
            parse_str = ''
            if isinstance(parse_result, (int,float,DiceDistribution)):
                parse_str = str(parse_result)
            expr = expr[:sidx] + parse_str + expr[eidx+1:]
        return expr
    
    def get_variables_dict(self) -> dict[str,str]:
        return self.parser.variables.get_variables()

    def get_constants_dict(self) -> dict[str,str]:
        return self.parser.variables.get_constants()
