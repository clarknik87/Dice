import re
import numpy as np

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
    die = die = np.vstack((probs,rolls))
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

    def __repr__(self):
        return self.expr