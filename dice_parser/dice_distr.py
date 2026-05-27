import re
import copy
import math
import numpy as np
from numpy.typing import NDArray
import random
from typing import Generator
from matplotlib.axes import Axes
from dataclasses import dataclass

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

@dataclass
class DiceStats:
    expr: str
    minimum: float
    maximum: float
    average: float
    stddev: float

    def __repr__(self):
        return f"\tMinimum: {self.minimum}" + \
        f"\tMaximum: {self.maximum}" + \
        f"\tAverage: {self.average:.2f}" + \
        f"\tStdDev:  {self.stddev:.2f} 66%[{self.average-self.stddev:.2f},{self.average+self.stddev:.2f}]"

# Dice are stored as a 2d numpy array.
# The first row [0] stores the rolls
# The second row stors the probability of that rolls
#
# A d4 would look like this:
#       [0.25, 0.25, 0.25, 0.25]]
#       [[1.  , 2.  , 3.  , 4.  ],

def convolveDice(die1:NDArray[np.float64], die2: NDArray[np.float64]) -> NDArray[np.float64]:
    probs = np.convolve(die1[0], die2[0])
    min_roll = int(die1[1][0]+die2[1][0])
    rolls = np.linspace(min_roll, min_roll+len(probs)-1, len(probs))
    die = np.vstack((probs,rolls))
    return die

def getNullDie() -> NDArray[np.float64]:
    probs = np.array([1])
    rolls = np.array([0])
    die = np.vstack((probs,rolls))
    return die

def getDieDistribution(numsides:int) -> NDArray[np.float64]:
    if numsides <= 0:
        raise ValueError(f"die cannot have {numsides} sides")
    probs = np.ones(numsides)*(1/numsides)
    rolls = np.linspace(1,numsides,numsides)
    die = np.vstack((probs,rolls))
    return die

def getDiceDistribution(numdice:int, numsides:int) -> NDArray[np.float64]:
    if numsides <= 0:
        raise ValueError(f"cannot create distirbution for {numsides} sided die")
    if numdice < 0:
        raise ValueError(f"cannot create distribution for {numdice} dice")
    if numdice == 0:
        return getNullDie()
    else:
        single_die = getDieDistribution(numsides)
        ret_die = single_die
        for _ in range(numdice-1):
            ret_die = convolveDice(ret_die,single_die)
        return ret_die
    
def getMaxDistribution(numdice:int, numsides:int) -> NDArray[np.float64]:
    if numsides <= 0:
        raise ValueError(f"cannot create distirbution for {numsides} sided die")
    if numdice < 0:
        raise ValueError(f"cannot create distribution for {numdice} dice")
    if numdice == 0:
        return getNullDie()
    else:
        probs = np.ones(numsides)
        rolls = rolls = np.linspace(1,numsides,numsides)
        px = 0
        pxprev = 0
        for x in range(1,numsides+1):
            px = x**numdice - pxprev
            probs[x-1] = px/(numsides**numdice)
            pxprev += px    
        die = np.vstack((probs,rolls))
        return die

def getMinDistribution(numdice:int, numsides:int) -> NDArray[np.float64]:
    if numsides <= 0:
        raise ValueError(f"cannot create distirbution for {numsides} sided die")
    if numdice < 0:
        raise ValueError(f"cannot create distribution for {numdice} dice")
    if numdice == 0:
        return getNullDie()
    else:
        probs = np.ones(numsides)
        rolls = rolls = np.linspace(1,numsides,numsides)
        px = 0
        pxprev = 0
        for x in range(numsides,-1,-1):
            px = x**numdice - pxprev
            probs[numsides-x-1] = -px/(numsides**numdice)
            pxprev += px   
        die = np.vstack((probs,rolls))
        return die

def accel_asc(n:int) -> Generator[list[int]]:
    # This algorithm generates all of the integer partitions for an integer n
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

def get_valid_integer_partitions(n:int, part_len:int, max_val:int, min_val:int) -> list[list[int]]:
    part_list = []
    for p in accel_asc(n):
        if len(p) == part_len and max(p)<=max_val and min(p)>=min_val:
            part_list.append(p)
    return part_list

def extend_partition_max(partition: list[int], roll_list: list[list[int]], numdice:int) -> None:
    if len(partition) == numdice:
        roll_list.append(partition)
    else:
        for s in range(1,min(partition)+1):
            extend_partition_max(partition+[s],roll_list,numdice)
    
def extend_partition_min(partition: list[int], roll_list: list[list[int]], numdice:int, numsides:int) -> None:
    if len(partition) == numdice:
        roll_list.append(partition)
    else:
        for s in range(max(partition), numsides+1):
            extend_partition_min(partition+[s],roll_list,numdice, numsides)

def getComplexMaxDistribution(numdice:int, totaldice:int, numsides:int) -> NDArray[np.float64]:
    if numsides <= 0:
        raise ValueError(f"cannot create distirbution for {numsides} sided die")
    if numdice < 0:
        raise ValueError(f"cannot create distribution for {numdice} dice")
    if numdice > totaldice:
        raise ValueError(f"cannot create distribution for max {numdice} of {totaldice} dice")
    if numdice == 0 or totaldice == 0:
        return getNullDie()
    else:
        pdf = getDiceDistribution(numdice, numsides)
        for idx,roll_result in enumerate(pdf[1]):
            total_permutations = 0
            roll_list = []
            int_partitions = get_valid_integer_partitions(int(roll_result), numdice, numsides, 1)
            for part in int_partitions:
                temp_roll_list = []
                extend_partition_max(part, temp_roll_list, totaldice)
                roll_list += temp_roll_list
            for roll in roll_list:
                temp_product = 1
                for d in range(1,numsides+1):
                    temp_product *= math.factorial(roll.count(d))
                total_permutations += math.factorial(totaldice)/temp_product 
            pdf[0][idx] = total_permutations/(numsides**totaldice)
        return pdf

def getComplexMinDistribution(numdice:int, totaldice:int, numsides:int) -> NDArray[np.float64]:
    if numsides <= 0:
        raise ValueError(f"cannot create distirbution for {numsides} sided die")
    if numdice < 0:
        raise ValueError(f"cannot create distribution for {numdice} dice")
    if numdice > totaldice:
        raise ValueError(f"cannot create distribution for max {numdice} of {totaldice} dice")
    if numdice == 0 or totaldice == 0:
        return getNullDie()
    else:
        pdf = getDiceDistribution(numdice, numsides)
        for idx,roll_result in enumerate(pdf[1]):
            total_permutations = 0
            roll_list = []
            int_partitions = get_valid_integer_partitions(int(roll_result), numdice, numsides, 1)
            for part in int_partitions:
                temp_roll_list = []
                extend_partition_min(part, temp_roll_list, totaldice, numsides)
                roll_list += temp_roll_list
            for roll in roll_list:
                temp_product = 1
                for d in range(1,numsides+1):
                    temp_product *= math.factorial(roll.count(d))
                total_permutations += math.factorial(totaldice)/temp_product
            pdf[0][idx] = total_permutations/(numsides**totaldice)
        return pdf

class DiceDistribution(object):  
    def __init__(self, expr:str|None = None, pdf:NDArray[np.float64]|None = None) -> None:
        if expr:
            self.expr = expr
            if re.match('[0-9]+d[0-9]+', expr): # nds form
                numdice  = int(expr.split("d")[0])
                numsides = int(expr.split("d")[1])
                self.pdf = getDiceDistribution(numdice, numsides)
            elif re.match('^adv$', expr):
                self.pdf = getMaxDistribution(2,20)        
            elif re.match(r'max\(\d+d\d+\)', expr):
                expr = expr.replace('max(','')
                expr = expr.replace(')','')
                numdice  = int(expr.split("d")[0])
                numsides = int(expr.split("d")[1])
                self.pdf = getMaxDistribution(numdice, numsides)
            elif re.match('^dis$', expr):
                self.pdf = getMinDistribution(2,20)
            elif re.match(r'min\(\d+d\d+\)', expr):
                expr = expr.replace('min(','')
                expr = expr.replace(')','')
                numdice  = int(expr.split("d")[0])
                numsides = int(expr.split("d")[1])
                self.pdf = getMinDistribution(numdice, numsides)
            elif re.match(r'max\(\d+,\d+d\d+\)', expr):
                expr = expr.replace('max(','')
                expr = expr.replace(')','')
                numdice = int(expr.split(",")[0])
                totaldice  = int(expr.split("d")[0].split(",")[1])
                numsides = int(expr.split("d")[1])
                self.pdf = getComplexMaxDistribution(numdice, totaldice, numsides)
            elif re.match(r'min\(\d+,\d+d\d+\)', expr):
                expr = expr.replace('min(','')
                expr = expr.replace(')','')
                numdice = int(expr.split(",")[0])
                totaldice  = int(expr.split("d")[0].split(",")[1])
                numsides = int(expr.split("d")[1])
                self.pdf = getComplexMinDistribution(numdice, totaldice, numsides)
            else:
                raise ValueError(f"unable to parse {expr} as dice formula")
        elif pdf:
            self.pdf = pdf
        else:
            raise ValueError("DiceDistribution requires either an expr string or a pdf NDArray")
    
    def roll(self) -> int:
        return random.choices(self.pdf[1],self.pdf[0], k=1)[0]
    
    def roll_full(self) -> tuple[int, float]:
        result:int = random.choices(self.pdf[1],self.pdf[0], k=1)[0]
        score:float = (self<=result)
        return result,score

    def __eq__(self,other: int|float|DiceDistribution) -> float: # type: ignore[reportIncompatibleMethodsOverride]
        if isinstance(other, int):
            score = 0.0
            for roll in range(len(self.pdf[1])):
                if self.pdf[1][roll] == other:
                    score += float(self.pdf[0][roll])
            return score
        elif isinstance(other, float):
            if other.is_integer():
                return self == int(other)
            else:
                raise ValueError(f"unable to compare with non-integer values {other}")
        elif isinstance(other, DiceDistribution):
            return self-other == 0
        raise TypeError(f"unable to compare with {type(other)}")

    def __ne__(self,other: int|float|DiceDistribution) -> float: # type: ignore[reportIncompatibleMethodsOverride]
        return 1-(self == other)

    def __le__(self,other: int|float|DiceDistribution) -> float:
        if isinstance(other, int):
            score = 0.0
            for roll in range(len(self.pdf[1])):
                if self.pdf[1][roll] > other:
                    break
                else:
                    score += float(self.pdf[0][roll])
            return score
        elif isinstance(other, float):
            if other.is_integer():
                return self <= int(other)
            else:
                raise ValueError(f"unable to compare with non-integer values {other}")
        elif isinstance(other, DiceDistribution):
            return self-other<=0
        raise TypeError(f"unable to compare with {type(other)}")

    def __lt__(self,other: int|float|DiceDistribution) -> float:
        if isinstance(other, int):
            score = 0.0
            for roll in range(len(self.pdf[1])):
                if self.pdf[1][roll] >= other:
                    break
                else:
                    score += float(self.pdf[0][roll])
            return score
        elif isinstance(other, float):
            if other.is_integer():
                return self < int(other)
            else:
                raise ValueError(f"unable to compare with non-integer values {other}")
        elif isinstance(other, DiceDistribution):
            return self-other<0
        raise TypeError(f"unable to compare with {type(other)}")

    def __ge__(self,other: int|float|DiceDistribution) -> float:
        return 1-(self < other)

    def __gt__(self,other: int|float|DiceDistribution) -> float:
        return 1-(self <= other)

    def __repr__(self) -> str:
        return self.expr
        
    def __neg__(self) -> DiceDistribution:
        ret_dice = copy.deepcopy(self)
        ret_dice.pdf[1] *= -1
        ret_dice.pdf = np.fliplr(ret_dice.pdf)
        ret_dice.expr = "-" + self.expr
        return ret_dice
        
    def __add__(self,other: int|float|DiceDistribution) -> DiceDistribution:
        if isinstance(other, DiceDistribution):
            ret_dice = copy.deepcopy(self)
            ret_dice.expr = self.expr + "+" + other.expr
            ret_dice.pdf = convolveDice(self.pdf,other.pdf)
            return ret_dice
        elif isinstance(other, int):
            ret_dice = copy.deepcopy(self)
            ret_dice.pdf[1] += other
            ret_dice.expr += "+" + str(other)
            return ret_dice
        elif isinstance(other, float):
            if other.is_integer():
                return self + int(other)
            else:
                raise ValueError(f"unable to sum with non-integer values {other}")
        raise TypeError(f"unable to sum with {type(other)}")

    def __radd__(self,other: int|float|DiceDistribution) -> DiceDistribution:
        return self + other

    def __sub__(self,other: int|float|DiceDistribution) -> DiceDistribution:
        if isinstance(other, DiceDistribution):
            ret_dice = copy.deepcopy(self)
            temp = copy.deepcopy(other)
            temp = -temp
            ret_dice.expr = self.expr + temp.expr
            ret_dice.pdf = convolveDice(self.pdf, temp.pdf)
            return ret_dice
        elif isinstance(other, int):
            ret_dice = copy.deepcopy(self)
            ret_dice.pdf[1] -= other
            ret_dice.expr += "-" + str(other)
            return ret_dice
        elif isinstance(other, float):
            if other.is_integer():
                return self - int(other)
            else:
                raise ValueError(f"unable to subtract with non-integer values {other}")
        raise TypeError(f"unable to subtract with {type(other)}")

    def __rsub__(self,other: int|float|DiceDistribution) -> DiceDistribution:
        return -self + other

    def __mul__(self,other: int|float|DiceDistribution) -> DiceDistribution:
        if isinstance(other, int):
            ret_dice = copy.deepcopy(self)
            ret_dice.expr = "(" + ret_dice.expr + ")" + "*" + str(other)
            pdf_length = int(self.pdf[1][-1])*other-int(self.pdf[1][0])*other+1
            probs = np.zeros(pdf_length)
            rolls = np.linspace(self.pdf[1][0]*other, self.pdf[1][-1]*other, pdf_length)
            for term in range(len(self.pdf[0])):
                probs[term*other] = self.pdf[0][term]
            ret_dice.pdf = np.vstack((probs,rolls))
            return ret_dice
        elif isinstance(other, float):
            if other.is_integer():
                return self*int(other)
            else:
                raise ValueError(f"unable to multiply with non-integer values {other}")
        else:
            raise TypeError(f"unable to multiply with {type(other)}")

    def __rmul__(self,other: int|float|DiceDistribution) -> DiceDistribution:
        return self * other

    def expected_value(self) -> float:
        ex = 0.0
        for term in range(len(self.pdf[0])):
            ex += self.pdf[0][term]*self.pdf[1][term]
        return ex
        
    def variance(self) -> float:
        ex = self.expected_value()
        var = 0.0
        for term in range(len(self.pdf[0])):
            var += self.pdf[0][term]*(ex-self.pdf[1][term])**2
        return var
        
    def standard_dev(self) -> float:
        return (self.variance()**0.5)
        
    def minimum(self) -> float:
        return self.pdf[1][0]
        
    def maximum(self) -> float:
        return self.pdf[1][-1]
    
    def print_stats(self) -> DiceStats:
        return DiceStats(
            expr=  self.expr,
            minimum = self.minimum(),
            maximum = self.maximum(),
            average = self.expected_value(),
            stddev = self.standard_dev()
        )
    
    def generate_plot(self, ax:Axes, color:str='b') -> None:
        ax.plot(self.pdf[1],self.pdf[0], color+'p', label=self.expr)
        ax.set_xlabel('roll outcome')
        ax.set_ylabel('probablity')
        #ax.grid(visible=True, axis='both')
        
