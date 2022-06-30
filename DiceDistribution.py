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
    pdf = getDieDistribution(numsides)
    for die in range(numdice-1):
        pdf = np.convolve(pdf,pdf)
    return pdf
    
def getMaxDistribution(numdice, numsides):
    pdf = {}
    return pdf

def getMinDistribution(numdice, numsides):
    pdf = {}
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