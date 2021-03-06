
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'statementleftEQUAL_TONOT_EQUAL_TOGREATER_THANGREATER_EQUALLESS_THANLESS_EQUALleftPLUSMINUSleftTIMESDIVIDErightUMINUSCOMMA DICE DIVIDE EQUALS EQUAL_TO GREATER_EQUAL GREATER_THAN LESS_EQUAL LESS_THAN LPAREN MINUS NAME NOT_EQUAL_TO NUMBER_DOUBLE NUMBER_INT PLUS RPAREN TIMES\n    statement : NAME EQUALS expression\n    \n    statement : expression\n    \n    expression : expression PLUS expression\n               | expression MINUS expression\n               | expression DIVIDE expression\n               | expression TIMES expression\n    \n    expression : MINUS expression %prec UMINUS\n    \n    expression : LPAREN expression RPAREN\n    \n    expressions : expressions COMMA expression\n               | expression\n               |\n    \n    expression : NAME LPAREN expressions RPAREN\n    \n    expression : DICE\n    \n    expression : expression EQUAL_TO expression\n               | expression NOT_EQUAL_TO expression\n               | expression GREATER_THAN expression\n               | expression GREATER_EQUAL expression\n               | expression LESS_THAN expression\n               | expression LESS_EQUAL expression\n    \n    expression : NUMBER_INT\n               | NUMBER_DOUBLE\n    \n    expression : NAME\n    '
    
_lr_action_items = {'NAME':([0,4,5,9,10,11,12,13,14,15,16,17,18,19,20,39,],[2,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'MINUS':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,],[4,-22,12,4,4,-13,-20,-21,4,4,4,4,4,4,4,4,4,4,4,4,-7,-22,12,12,12,-3,-4,-5,-6,12,12,12,12,12,12,-8,-12,4,12,]),'LPAREN':([0,2,4,5,9,10,11,12,13,14,15,16,17,18,19,20,22,39,],[5,10,5,5,5,5,5,5,5,5,5,5,5,5,5,5,10,5,]),'DICE':([0,4,5,9,10,11,12,13,14,15,16,17,18,19,20,39,],[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,]),'NUMBER_INT':([0,4,5,9,10,11,12,13,14,15,16,17,18,19,20,39,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'NUMBER_DOUBLE':([0,4,5,9,10,11,12,13,14,15,16,17,18,19,20,39,],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,]),'$end':([1,2,3,6,7,8,21,22,24,27,28,29,30,31,32,33,34,35,36,37,38,],[0,-22,-2,-13,-20,-21,-7,-22,-1,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,]),'EQUALS':([2,],[9,]),'PLUS':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,11,-13,-20,-21,-7,-22,11,11,11,-3,-4,-5,-6,11,11,11,11,11,11,-8,-12,11,]),'DIVIDE':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,13,-13,-20,-21,-7,-22,13,13,13,13,13,-5,-6,13,13,13,13,13,13,-8,-12,13,]),'TIMES':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,14,-13,-20,-21,-7,-22,14,14,14,14,14,-5,-6,14,14,14,14,14,14,-8,-12,14,]),'EQUAL_TO':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,15,-13,-20,-21,-7,-22,15,15,15,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,15,]),'NOT_EQUAL_TO':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,16,-13,-20,-21,-7,-22,16,16,16,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,16,]),'GREATER_THAN':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,17,-13,-20,-21,-7,-22,17,17,17,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,17,]),'GREATER_EQUAL':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,18,-13,-20,-21,-7,-22,18,18,18,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,18,]),'LESS_THAN':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,19,-13,-20,-21,-7,-22,19,19,19,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,19,]),'LESS_EQUAL':([2,3,6,7,8,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-22,20,-13,-20,-21,-7,-22,20,20,20,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,20,]),'RPAREN':([6,7,8,10,21,22,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-13,-20,-21,-11,-7,-22,37,38,-10,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,-9,]),'COMMA':([6,7,8,10,21,22,25,26,27,28,29,30,31,32,33,34,35,36,37,38,40,],[-13,-20,-21,-11,-7,-22,39,-10,-3,-4,-5,-6,-14,-15,-16,-17,-18,-19,-8,-12,-9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,4,5,9,10,11,12,13,14,15,16,17,18,19,20,39,],[3,21,23,24,26,27,28,29,30,31,32,33,34,35,36,40,]),'expressions':([10,],[25,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> NAME EQUALS expression','statement',3,'p_statement_assign','Dice.py',32),
  ('statement -> expression','statement',1,'p_statement_expression','Dice.py',38),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','Dice.py',49),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','Dice.py',50),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','Dice.py',51),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','Dice.py',52),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','Dice.py',65),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','Dice.py',71),
  ('expressions -> expressions COMMA expression','expressions',3,'p_expressions','Dice.py',77),
  ('expressions -> expression','expressions',1,'p_expressions','Dice.py',78),
  ('expressions -> <empty>','expressions',0,'p_expressions','Dice.py',79),
  ('expression -> NAME LPAREN expressions RPAREN','expression',4,'p_expression_function','Dice.py',120),
  ('expression -> DICE','expression',1,'p_expression_dice','Dice.py',184),
  ('expression -> expression EQUAL_TO expression','expression',3,'p_comparison_dice','Dice.py',190),
  ('expression -> expression NOT_EQUAL_TO expression','expression',3,'p_comparison_dice','Dice.py',191),
  ('expression -> expression GREATER_THAN expression','expression',3,'p_comparison_dice','Dice.py',192),
  ('expression -> expression GREATER_EQUAL expression','expression',3,'p_comparison_dice','Dice.py',193),
  ('expression -> expression LESS_THAN expression','expression',3,'p_comparison_dice','Dice.py',194),
  ('expression -> expression LESS_EQUAL expression','expression',3,'p_comparison_dice','Dice.py',195),
  ('expression -> NUMBER_INT','expression',1,'p_expression_number','Dice.py',212),
  ('expression -> NUMBER_DOUBLE','expression',1,'p_expression_number','Dice.py',213),
  ('expression -> NAME','expression',1,'p_expression_name','Dice.py',219),
]
