import re
import copy
import math
import numpy as np
import random

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

# Dice are stored as a 2d numpy array.
# The first row [0] stores the rolls
# The second row stors the probability of that rolls
#
# A d4 would look like this:
#       [0.25, 0.25, 0.25, 0.25]]
#       [[1.  , 2.  , 3.  , 4.  ],

def convolveDice(die1,die2):
    probs = np.convolve(die1[0], die2[0])
    min_roll = int(die1[1][0]+die2[1][0])
    rolls = np.linspace(min_roll, min_roll+len(probs)-1, len(probs))
    die = np.vstack((probs,rolls))
    return die

def getDieDistribution(numsides):
    probs = np.ones(numsides)*(1/numsides)
    rolls = np.linspace(1,numsides,numsides)
    die = np.vstack((probs,rolls))
    return die

def getDiceDistribution(numdice, numsides):
    single_die = getDieDistribution(numsides)
    ret_die = single_die
    for die in range(numdice-1):
        ret_die = convolveDice(ret_die,single_die)
    return ret_die
    
def getMaxDistribution(numdice, numsides):
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

def getMinDistribution(numdice, numsides):
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

def accel_asc(n):
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

def get_valid_integer_partitions(n, part_len, max_val, min_val):
    part_list = []
    for p in accel_asc(n):
        if len(p) == part_len and max(p)<=max_val and min(p)>=min_val:
            part_list.append(p)
    return part_list

def extend_partition_max(partition, roll_list, numdice):
    if len(partition) == numdice:
        roll_list.append(partition)
    else:
        for s in range(1,min(partition)+1):
            extend_partition_max(partition+[s],roll_list,numdice)
    
def extend_partition_min(partition, roll_list, numdice, numsides):
    if len(partition) == numdice:
        roll_list.append(partition)
    else:
        for s in range(max(partition), numsides+1):
            extend_partition_min(partition+[s],roll_list,numdice, numsides)

def getComplexMaxDistribution(numdice, totaldice, numsides):
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

def getComplexMinDistribution(numdice, totaldice, numsides):
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
    def __init__(self,expr: str = 'unknown',pdf = np.array([])) -> None:
        self.expr = expr
        if re.match('[0-9]+d[0-9]+', expr): # nds form
            numdice  = int(expr.split("d")[0])
            numsides = int(expr.split("d")[1])
            self.pdf = getDiceDistribution(numdice, numsides)
        elif re.match('adv', expr):
            self.pdf = getMaxDistribution(2,20)        
        elif re.match('max\(\d+d\d+\)', expr):
            expr = expr.replace('max(','')
            expr = expr.replace(')','')
            numdice  = int(expr.split("d")[0])
            numsides = int(expr.split("d")[1])
            self.pdf = getMaxDistribution(numdice, numsides)
        elif re.match('dis', expr):
            self.pdf = getMinDistribution(2,20)
        elif re.match('max\(\d+d\d+\)', expr):
            expr = expr.replace('min(','')
            expr = expr.replace(')','')
            numdice  = int(expr.split("d")[0])
            numsides = int(expr.split("d")[1])
            self.pdf = getMinDistribution(numdice, numsides)
        elif re.match('max\(\d+,\d+d\d+\)', expr):
            expr = expr.replace('max(','')
            expr = expr.replace(')','')
            numdice = int(expr.split(",")[0])
            totaldice  = int(expr.split("d")[0].split(",")[1])
            numsides = int(expr.split("d")[1])
            self.pdf = getComplexMaxDistribution(numdice, totaldice, numsides)
        elif re.match('min\(\d+,\d+d\d+\)', expr):
            expr = expr.replace('min(','')
            expr = expr.replace(')','')
            numdice = int(expr.split(",")[0])
            totaldice  = int(expr.split("d")[0].split(",")[1])
            numsides = int(expr.split("d")[1])
            self.pdf = getComplexMinDistribution(numdice, totaldice, numsides)
        else:
            self.pdf = pdf
    
    def roll(self):
        result = int(random.choices(self.pdf[1],self.pdf[0], k=1)[0])
        return "{} [{:.2f}%]".format(result,(self<result)*100)

    def __eq__(self,other):
        score = 0.0
        if isinstance(other, int):
            for roll in range(len(self.pdf[1])):
                if self.pdf[1][roll] == other:
                    score = self.pdf[0][roll]
                    return score;
        elif isinstance(other, float):
            return self == int(other)
        elif isinstance(other, DiceDistribution):
            return self-other == 0;
        return score

    def __ne__(self,other):
        return 1-(self == other)

    def __le__(self,other):
        score = 0.0
        if isinstance(other, int):
            for roll in range(len(self.pdf[1])):
                if self.pdf[1][roll] > other:
                    break
                else:
                    score += self.pdf[0][roll]
        elif isinstance(other, float):
            return self <= int(other)
        elif isinstance(other, DiceDistribution):
            return self-other<=0;
        return score

    def __lt__(self,other):
        score = 0.0
        if isinstance(other, int):
            for roll in range(len(self.pdf[1])):
                if self.pdf[1][roll] >= other:
                    break
                else:
                    score += self.pdf[0][roll]
        elif isinstance(other, float):
            return self < int(other)
        elif isinstance(other, DiceDistribution):
            return self-other<0;
        return score

    def __ge__(self,other):
        return 1-(self < other)

    def __gt__(self,other):
        return 1-(self <= other)

    def __repr__(self):
        return self.expr
        
    def __neg__(self):
        ret_dice = copy.deepcopy(self)
        ret_dice.pdf[1] *= -1
        ret_dice.pdf = np.fliplr(ret_dice.pdf)
        ret_dice.expr = "-" + self.expr
        return ret_dice
        
    def __add__(self,other):
        ret_dice = copy.deepcopy(self)
        if isinstance(other, DiceDistribution):
            ret_dice.expr = self.expr + "+" + other.expr
            ret_dice.pdf = convolveDice(self.pdf,other.pdf)
        elif isinstance(other, int):
            ret_dice.pdf[1] += other
            ret_dice.expr += "+" + str(other)
        elif isinstance(other, float):
            return self + int(other)
        return ret_dice

    def __radd__(self,other):
        return self + other

    def __sub__(self,other):
        ret_dice = copy.deepcopy(self)
        if isinstance(other, DiceDistribution):
            temp = copy.deepcopy(other)
            temp = -temp
            ret_dice.expr = self.expr + temp.expr
            ret_dice.pdf = convolveDice(self.pdf, temp.pdf)
        elif isinstance(other, int):
            ret_dice.pdf[1] -= other
            ret_dice.expr += "-" + str(other)
        elif isinstance(other, float):
            return self - int(other)
        return ret_dice

    def __rsub__(self,other):
        return -self + other

    def __mul__(self,other):
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
            return self*int(other)
        else:
            raise NotImplemented

    def __rmul__(self,other):
        return self * other

    def expected_value(self):
        ex = 0.0
        for term in range(len(self.pdf[0])):
            ex += self.pdf[0][term]*self.pdf[1][term]
        return ex
        
    def variance(self):
        ex = self.expected_value()
        var = 0.0
        for term in range(len(self.pdf[0])):
            var += self.pdf[0][term]*(ex-self.pdf[1][term])**2
        return var
        
    def standard_dev(self):
        return (self.variance()**0.5)
        
    def minimum(self):
        return self.pdf[1][0]
        
    def maximum(self):
        return self.pdf[1][-1]
    
    def print_stats(self):
        expected = self.expected_value()
        stddev = self.standard_dev()
        print("\tMinimum: {}".format(self.minimum()))
        print("\tMaximum: {}".format(self.maximum()))
        print("\tAverage: {:.2f}".format(expected))
        print("\tStdDev:  {:.2f} 66%[{:.2f},{:.2f}]".format(stddev,expected-stddev,expected+stddev))
    
    def generate_plot(self, ax, color='b'):
        ax.plot(self.pdf[1],self.pdf[0], color+'p', label=self.expr)
        ax.set_xlabel('roll outcome')
        ax.set_ylabel('probablity')
        #ax.grid(visible=True, axis='both')
        
