# Dice Python Utility

import os
import random
import re

#all stat functions return min,max,E,V
def statMax(numdice,numsides):
    min = 1
    max = numsides
    ex = 0
    px = 0
    pxprev = 0
    for x in range(numsides+1):
        px = x**numdice - pxprev
        ex += (px/(numsides**numdice))*x
        pxprev += px
    var = 0
    px = 0
    pxprev = 0
    for x in range(numsides+1):
        px = x**numdice - pxprev
        var += (px/(numsides**numdice))*((x - ex)**2)
        pxprev += px
    return min,max,ex,var

def statMin(numdice,numsides):
    min = 1
    max = numsides
    ex = 0
    var = 0
    px = 0
    pxprev = 0
    for x in range(numsides,0,-1):
        px = x**numdice - pxprev
        ex += (px/(numsides**numdice))*x
        pxprev += px
    var = 0
    px = 0
    pxprev = 0
    for x in range(numsides,0,-1):
        px = (numsides - x +1)**numdice - pxprev
        var += (px/(numsides**numdice))*((x - ex)**2)
        pxprev += px
    return min,max,ex,var

def statDice(numdice,numsides):
    min = numdice
    max = numdice*numsides
    ex = (numdice*(numsides+1))/2
    var = 0
    for i in range(1,numsides+1):
        var += (i-ex/numdice)**2
    var *= numdice/numsides
    return min,max,ex,var


#sum all rolls
def evalDice(numdice,numsides):
    sum = 0
    allrolls = []
    for rolls in range(numdice):
        roll = random.randrange(1,numsides+1)
        sum += roll
        allrolls.append(roll)
    return sum, allrolls

#choose the highest roll    
def evalMax(numdice,numsides):
    max = 1
    allrolls = []
    for rolls in range(numdice):
        roll = random.randrange(1,numsides+1)
        allrolls.append(roll)
        if roll > max:
            max = roll
    return max,allrolls

#choose the lowest roll
def evalMin(numdice,numsides):
    min = numsides+1
    allrolls = []
    for rolls in range(numdice):
        roll = random.randrange(1,numsides+1)
        allrolls.append(roll)
        if roll < min:
            min = roll
    return min,allrolls

def calcStats( expr ):
    firstTerm = True
    operators = []
    minimum = 0
    maximum = 0
    expected = 0
    variance = 0
    
    #remove "stats(" ")"
    expr = re.split("\((.+)\)",expr)
    innerexpr = expr[1]
    for token in re.split('([+-])', innerexpr):
        tokenmin = 0
        tokenmax = 0
        tokenex = 0
        tokenvar = 0
        if token == "+" or token == "-":
            operators.append(token)
            continue
        elif token.startswith("max("):
            temp = token
            temp = temp.replace("max(", "")
            temp = temp.replace(")","")
            tokenmin,tokenmax,tokenex,tokenvar = statMax(int(temp.split("d")[0]), int(temp.split("d")[1]))
        elif token.startswith("min("):
            temp = token
            temp = temp.replace("min(", "")
            temp = temp.replace(")","")
            tokenmin,tokenmax,tokenex,tokenvar = statMin(int(temp.split("d")[0]), int(temp.split("d")[1]))
        elif token.startswith("adv"):
            tokenmin,tokenmax,tokenex,tokenvar = statMax(2, 20)
        elif token.startswith("dis"):
            tokenmin,tokenmax,tokenex,tokenvar = statMin(2, 20)
        elif "d" in token:
            tokenmin,tokenmax,tokenex,tokenvar = statDice(int(token.split("d")[0]), int(token.split("d")[1]))
        else: #a constant
            tokenmin = int(token)
            tokenmax = int(token)
            tokenex = int(token)
            tokenvar = 0
            
   
        if len(operators) == 1 or not firstTerm:
            if operators[0] == '-':
                minimum -= tokenmin
                maximum -= tokenmax
                expected -= tokenex
                variance -= tokenvar
            else:
                minimum += tokenmin
                maximum += tokenmax
                expected += tokenex
                variance += tokenvar
            operators.clear()
        else:
            minimum += tokenmin
            maximum += tokenmax
            expected += tokenex
            variance += tokenvar
    
    stddev = variance**0.5
    print("\tMinimum: {}".format(minimum))
    print("\tMaximum: {}".format(maximum))
    print("\tAverage: {:.2f}".format(expected))
    print("\tStdDev:  {:.2f} 66%[{:.2f},{:.2f}]".format(stddev,expected-stddev,expected+stddev))
    return 

def rollDice( expr ):
    operators = []
    finalresult = 0
    response = ""
    firstTerm = True
    for token in re.split('([+-])', expr):
        result = 0
        text = ""
        if token == "+" or token == "-":
            operators.append(token)
            continue
        elif token.startswith("max("):
            temp = token
            temp = temp.replace("max(", "")
            temp = temp.replace(")","")
            result, text = evalMax(int(temp.split("d")[0]), int(temp.split("d")[1]))
            text = "max" + str(text)
        elif token.startswith("min("):
            temp = token
            temp = temp.replace("min(", "")
            temp = temp.replace(")","")
            result, text = evalMin(int(temp.split("d")[0]), int(temp.split("d")[1]))
            text = "min" + str(text)
        elif token.startswith("adv"):
            result, text = evalMax(2, 20)
            text = "adv" + str(text)
        elif token.startswith("dis"):
            result, text = evalMin(2, 20)
            text = "dis" + str(text)
        elif "d" in token:
            result, text = evalDice(int(token.split("d")[0]), int(token.split("d")[1]))
        else: #a constant
            result = int(token)
   
        if len(operators) == 1 or not firstTerm:
            if operators[0] == '-':
                finalresult -= result
                response += "- {}{} ".format(str(text), result)
            else:
                finalresult += result
                response += "+ {}{} ".format(str(text), result)
            operators.clear()
        else:
            finalresult += result
            response += "{}{} ".format(str(text), result)
    
    print("{} = {}".format(response, finalresult))
    return
    
        
     
def parseInput( str ):
    try:
        if str.startswith("stats("):        
            calcStats(str)
        else:
            rollDice(str)
    except:
        pass
        

def main():
    try:
        inputText = ""
        while "quit" not in inputText and "exit" not in inputText:
            if "clear" in inputText:
                os.system('cls')
            if "*" in inputText or "/" in inputText:
                print(eval(inputText))
            print(">> ", end=" ")
            inputText = input()
            if "quit" not in inputText and "exit" not in inputText and len(inputText) > 0:
                parseInput(inputText)
    except KeyboardInterrupt:
        print("Exiting Dice.py...")
        
        
    
if __name__ == "__main__":
    main()