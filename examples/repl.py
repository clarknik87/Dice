import os
import sys
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dice_parser.parser import DiceParser
from dice_parser.dice_distr import DiceDistribution

def main() -> None:
    p = DiceParser()
    while True:
        expr = input('>> ')
        if "clear" in expr:
                os.system('cls')
        elif 'quit' in expr:
            return
        elif expr != '':
            result = p.parse(expr)
            if isinstance(result, DiceDistribution):
                result, score = result.roll_full()
                score *= 100
                print(f"{result} [{score:.2f}%]")
            elif isinstance(result, float):
                print('{:.4f}'.format(result))
            elif isinstance(result, tuple) and list(map(type, result)) == [Figure, Axes]:
                 plt.show()
            elif result != None:
                print(result)

if __name__ == '__main__':
     main()
