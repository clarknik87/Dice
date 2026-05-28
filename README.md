# Dice
Dice rolling and probability string parsing utility.
For an interactive demonstration see `examples/repl.py`. Parser syntax is exaplined below.

## Arithmetic
This parser functions as a basic calculator. It supports integer and floating point operations, `+,-,*,/` as well as various built-in functions, `sqrt`, `ceil`, `round`, `floor`, `pow`, and type conversions `int`, and `floor`.

### Examples
- `1+5` -> `7`
- `1.5*4` -> `6`
- `10/2` -> `5`
- `sqrt(16)` -> `4`
- `ceil(4.5)` -> `5`
- `round(4.5)` -> `5`
- `floor(4.5)` -> `4`
- `pow(2,4)` -> `16`
- `int(4.8)` -> `4`
- `float(6)` -> `6.0`

## Basic Dice Formulas
This parser also treats dice formulas as first class objects. All dice can be entered as a formula of <number of dice>d<number of sides>. To roll a simple six sided die enter 1d6. To roll 2 six sided die and add them enter 1d6 + 1d6, or more simply 2d6. 

## Complex Dice Formulas
The parser also supports max(nds) or min(nds) functions. This is for rolling n s-sided die and selecting the highest/lowest roll. For max(2d20) and min(2d20) the abbreviations adv and dis are available. The parser also recognizes the syntax max(x,nds) or min(x,nds). This represents rolling n s-sided dice and summing the highest or lowest x dice. max(3,4d6) for example returns the distribution resulting from rolling 4 6-sided dice and summing the highest 3. 

## Dice Arithmetic
The parser supports arithmetic operations combining integers and dice formulas. Currently the parser supports addition, subtraction, and multiplication with dice formulas. For example `1d20+7`, `2d4-3`, `adv*2`, or `max(2,3d20)+7`. The operators are commutative as well, ie `7+1d20` is just as valid as `1d20+7`. Addition and subtraction are supported for two dice formulas. `1d4 + 1d6` or `1d20-1d4` are both valid and return the corresponding distributions. Negation is also supported, for example `-1d4`. Multiplication between two dice formulas is not currently supported. Division is not supported for neither two dice nor dice and an integer/float.

## Dice Comparisons
The parser also supports comparison operations `==`, `!=`, `<`, `<=`, `>`, and `>=` using integers and/or dice formulas. Comparisons return the probability (a float in the range [0.0-1.0]) that the comparison is true. For example `1 > 0` is never true and thus returns `0.0`. `1d20 > 1` is true 95% of the time and therefore returns `0.95`. Again complex formulas and simple addition are supported. `1d20+1>3` will return `0.9`. Comparison of a dice formula with a floating point value is only supported if that value can be converted to an integer.

## Dice Functions
Enclosing a dice expression in `roll(<expr>)` will cause the parser to simulate a roll of that dice expression and return an integer value at (weighted) random from the corresponding distribution.

Enclosing a dice expression in `stats(<expr>)` will return the minimum roll, maximum roll, average (expected value) roll, and the standard deviation of the distribution as a `DiceStats` dataclass.

Enclosing a dice expression in `plot(<expr>)` causes the parser to return a matplotlib tuple containing a figure and axes that can be displayed with the `plt.show()` command if desired. You can also plot a list of expressions and have them shown on a single plot. This is very useful for visually comparing distributions. For example `plot(1d20, adv, dis)` will return a figure,axes tuple ready to display all three distributions.

## Constants and Variables
The parser stores two internal dictionaries for constants and variables. This allows a user to alias larger dice formulas to conventient names. Both constants and variables are read the same, but only variables can have their alias changed at runtime. Contants must be supplied to the parser when the parser class is constructed. To assign a variable use the following syntax: `fireball = 6d8`. The parser will return `None` if successful. Later the user can simply type `roll(fireball)` instead of `roll(6d8)`. You can assign more complicated formulas: `perception = adv+6+1d4+1d6`. You can even nest aliases. `dex = 5` followed by `acrobatics = 1d20+dex` is valid. 

## Error Codes
Invalid parser input should return an error code of type `ParseError` found in parser.py. These are specific, though minimally descriptive of the various parsing errors that may occur.

# Unit Tests
The parser can be tested by simply calling `python /test/unit_test.py`. The unit tests rely on the built in unittest library and should print a brief summary of the test results.
