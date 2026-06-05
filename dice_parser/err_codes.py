class UndefinedFunctionError(Exception):
    def __init(self, err:str = ''):
        self.err = err

class InvalidFunctionArguments(Exception):
    def __init__(self, err:str = ''):
        self.err = err

class SyntaxError(Exception):
    def __init__(self, err:str = ''):
        self.err = err