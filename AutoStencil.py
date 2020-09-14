import numpy as _np
import RationalAlgebra as _ra
from math import factorial as _factorial
from math import gcd as _gcd

def parseStringInputs(stencilString, dimensionString):
    try:
        stencilInts = _makeStencilInts(stencilString)
        stencilSuccess = True
    except:
        latexString = ("$$\\text{Please enter a comma-separated list of"
                       "values for the locations of sampled points.}$$")
        stencilSuccess = False
    try:
        dimensionInt = _makeDimInt(dimensionString)
        dimensionSuccess = True
    except:
        latexString = ("$$\\text{Please enter a non-negative integer "
                       "derivative order.}$$")
        dimensionSuccess = False
    
    if stencilSuccess and dimensionSuccess:
        if dimensionInt >= len(stencilInts):
            latexString = ("$$\\text{Please enter a derivative order that is "
                           "less than the number of points in your stencil.}$$")
            codeString = ''
        else:
            print(stencilInts)
            latexString = stencilLatex(stencilInts, dimensionInt, 'f', 'x', 'h')
            codeString = stencilCode(stencilInts, dimensionInt, 'f', 'i', 'h')
            print(latexString)
    else:
        codeString = ''
    return latexString, codeString
def _makeStencilInts(inString):
    splitString = inString.replace(';',' ').replace(',',' ').split()
    nums = list(map(lambda x: int(float(x)), splitString))
    nums = sorted(list(set(nums)))
    return _np.array(nums)
def _makeDimInt(inString):
    return int(float(inString))
def stencilCode(C, d, functionName, functionVar, stepVar):
    # Calculate stencil
    newNumerators, lcmDenom = computeStencil(C, d)
    
    # Make LHS
    lhsString = "d" + str(d) + functionName + (
                "[" + functionVar + "] = " )
    
    # Make numerator
    nString = "("
    for i in range(len(C)):
        if newNumerators[i] != 0:
            multiplierAbs = abs(newNumerators[i])
            multiplier = "" if multiplierAbs==1 else str(multiplierAbs) + "*"
            multiplierSign = "-" if newNumerators[i]<0 else "+"

            indexAbs = abs(C[i])
            indexSign = "-" if C[i]<0 else "+"
            indexAdd = "" if C[i]==0 else indexSign + str(indexAbs)

            addString = multiplierSign + multiplier + (
                        functionName + "[" + functionVar ) + (
                        indexAdd + "]" )
            nString += addString
    
    nString += ")"
    nString = nString.replace("(+", "(")
    
    # Make denominator
    multiplier = "" if lcmDenom==1 else str(lcmDenom) + "*"
    powerString = "" if d==1 else "^" + str(d)
    dString = "(" + multiplier + stepVar + powerString + ")"
    
    # Make expression
    fullExp = lhsString + nString + "/" + dString
    
    return fullExp
def stencilLatex(C, d, functionName, functionVar, stepVar):
    # Calculate stencil
    newNumerators, lcmDenom = computeStencil(C, d)
    
    # Make LHS
    lhsString = "\\frac{\\partial^" + str(d) + (
                " " + functionName + "}{\\partial " + functionVar ) + (
                "^" + str(d) + "}" )
    
    # Make numerator
    nString = "{"
    for i in range(len(C)):
        if newNumerators[i] != 0:
            multiplierAbs = abs(newNumerators[i])
            multiplier = "" if multiplierAbs==1 else str(multiplierAbs)
            multiplierSign = "-" if newNumerators[i]<0 else "+"

            indexAbs = abs(C[i])
            indexSign = "-" if C[i]<0 else "+"
            indexString = "" if indexAbs==1 else str(indexAbs)
            indexAdd = "" if C[i]==0 else indexSign + indexString + stepVar

            addString = multiplierSign + multiplier + (
                       functionName + "(" + functionVar ) + (
                       indexAdd + ")" )
            nString += addString

    nString += "}"
    nString = nString.replace("{+","{")
    
    # Make denominator
    multiplier = "" if lcmDenom==1 else str(lcmDenom)
    powerString = "" if d==1 else "^" + str(d)
    dString = "{" + multiplier + stepVar + powerString + "}"
    
    # Make expression
    fullExp = '$$' + lhsString + "\\approx \\frac" + nString + dString + '$$'
    
    return fullExp
def computeStencil(C, d):
    N = len(C)
    if d >= N:
        raise ValueError(
            "Derivative order must be less than the number of points in the stencil.")
    
    A = _vectorMultiplicand(d, N)
    M = _matrixMultiplier(C, N)
    ratA = _ra.RationalVector(A)
    ratM = _ra.RationalMatrix(M)
    res = _ra.inv(ratM) @ ratA
    newNumerators, lcmDenom = _integerRepresentation(res)
    return newNumerators, lcmDenom
def _vectorMultiplicand(d, N):
    c = _np.zeros((N, 1))
    c = c.astype(int)
    c[d] = _factorial(d)
    return c
def _matrixMultiplier(C, N):
    M = _np.zeros((N, N))
    M = M.astype(int)
    exponentRange = range(N)
    for i in exponentRange:
        M[:,i] = [C[i]**x for x in exponentRange]
    return M
def _integerRepresentation(resultArray):
    numer = _np.array(list(
        map(lambda x: x[0].numerator, resultArray.value)))
    denom = _np.array(list(
        map(lambda x: x[0].denominator, resultArray.value)))
    lcmDenom = _lcmRec(denom)
    numFactor = _np.array(list(map(lambda x: lcmDenom // x, denom)))
    newNumerators = numer * numFactor
    return newNumerators, lcmDenom
def _lcm2(a, b):
    return abs(a*b) // _gcd(a, b)
def _lcmRec(intList):
    if len(intList) == 2:
        return _lcm2(intList[0], intList[1])
    else:
        return _lcm2(intList[0], _lcmRec(intList[1:]))


    
