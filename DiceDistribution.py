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


class DiceDistribution(object):  
    def __init__(self,expr: str = 'unknown',pdf = np.array([])) -> None:
        self.expr = expr
        if re.match('[0-9]+d[0-9]+', expr): # nds form
            numdice  = int(expr.split("d")[0])
            numsides = int(expr.split("d")[1])
            self.pdf = getDiceDistribution(numdice, numsides)
        elif re.match('adv', expr):
            self.pdf = getMaxDistribution(2,20)        
        elif re.match('max\(.+\)', expr):
            expr = expr.replace('max(','')
            expr = expr.replace(')','')
            numdice  = int(expr.split("d")[0])
            numsides = int(expr.split("d")[1])
            self.pdf = getMaxDistribution(numdice, numsides)
        elif re.match('dis', expr):
            self.pdf = getMinDistribution(2,20)
        elif re.match('min\(.+\)', expr):
            expr = expr.replace('min(','')
            expr = expr.replace(')','')
            numdice  = int(expr.split("d")[0])
            numsides = int(expr.split("d")[1])
            self.pdf = getMinDistribution(numdice, numsides)
        else:
            self.pdf = pdf
    
    def roll(self):
        result = int(random.choices(self.pdf[1],self.pdf[0], k=1)[0])
        score = 0.0
        for roll in range(len(self.pdf[1])):
            if self.pdf[1][roll] > result:
                break
            else:
                score += self.pdf[0][roll]
        return "{} [{:.2f}%]".format(result,score*100)

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
        
