from ply.lex import Lexer
from ply.yacc import LRParser
from graphlib import TopologicalSorter
from dice_parser.dice_distr import DiceDistribution

_builtin_funcs: set[str] = {
	'roll',
	'stats',
	'sqrt',
	'ceil',
	'round',
	'floor',
	'pow',
	'int',
	'float',
}

class KeyRedefinitionError(Exception):
    def __init__(self, str:str='') -> None:
        self.str = str

class UndefindedDependencyError(Exception):
    def __init__(self, str:str='') -> None:
        self.str = str

class VariableKeyError(Exception):
    def __init__(self, str:str='') -> None:
        self.str = str

class user_var:
    def __init__(self, value:int|float|DiceDistribution, expr:str, dependencies:set[str], const:bool=False) -> None:
        self.value = value
        self.expr = expr
        self.const = const
        self.dependencies = dependencies

class var_graph:
    def __init__(self, lexer:Lexer, parser:LRParser) -> None:
        self.lexer = lexer
        self.parser = parser
        self.graph: dict[str,user_var] = {}
    
    def init_variables(self, vars:dict[str,str]={}, consts:dict[str,str]={}) -> None:
        if consts.keys() & vars.keys():
            raise RuntimeError(f"cannot instantiate var_graph, constants and variables share keys: {consts.keys() & vars.keys()}")
        eval_dict = {k : self._lex_dependencies(str(v)) for k,v in (consts|vars).items()}
        eval_order = TopologicalSorter(eval_dict).static_order()
        for i in eval_order:
            if i in consts.keys():
                self.graph[i] = user_var(
                        self.parser.parse(str(consts[i])),
                        consts[i],
                        self._lex_dependencies(str(consts[i])),
                        True
                    )
            elif i in vars.keys():
                    self.graph[i] = user_var(
                        self.parser.parse(str(vars[i])),
                        vars[i],
                        self._lex_dependencies(str(vars[i])),
                        False
                    )
    
    def __len__(self) -> int:
        return len(self.graph)
    
    def __getitem__(self, key:str) -> user_var:
        if key not in self.graph.keys():
            raise VariableKeyError(f"{key} not found in variable map")
        else:
            return self.graph[key]

    def _lex_dependencies(self, expr:str) -> set[str]:
        # use the lexer to extract all NAME tokens from the expression
        self.lexer.input(expr)
        return {e.value for e in self.lexer if e.type == 'NAME' and e.value not in _builtin_funcs}

    def _verify_graph(self) -> None:
        # check for cyclical dependencies, raises CycleError if found
        TopologicalSorter({k : v.dependencies for k,v in self.graph.items()}).prepare()
        # check for undefined dependencies
        for node in self.graph.values():
            for d in node.dependencies:
                if d not in self.graph.keys():
                    raise UndefindedDependencyError(f'undefined variable/constant: {d}')

    def _update_dependencies(self, key:str) -> None:
        update_list = [key]
        for i in update_list:
            # search graph for nodes that contain i, 
            # if found reparse the value and add that node's key to the update list
            for k,v in self.graph.items():
                if i in v.dependencies:
                    v.value = self.parser.parse(v.expr)
                    update_list.append(k)
    
    def _add_node(self, key:str, expr:str, const:bool) -> None:
        update_needed = False
        if key in self.graph.keys():
            if self.graph[key].const:
                raise KeyRedefinitionError(f'cannot redefine {key}')
            update_needed = True
        self.graph[key] = user_var(self.parser.parse(expr), expr, self._lex_dependencies(expr), const)
        self._verify_graph()
        if update_needed:
            self._update_dependencies(key)
    
    def add_var(self, key:str, expr:str) -> None:
        self._add_node(key, expr, False)
    
    def add_const(self, key:str, expr:str) -> None:
        self._add_node(key, expr, True)

    def get_variables(self) -> dict[str,str]:
        return {k : v.expr for k,v in self.graph.items() if not v.const}

    def get_constants(self) -> dict[str,str]:
        return {k : v.expr for k,v in self.graph.items() if v.const}
    
