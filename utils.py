import numpy as np
from fractions import Fraction
def checkVector(V):
    if isVector(V) is not True:
        raise ValueError('Not vector.')
def isVector(V):
    oneDim1 = any(x == 1 for x in V.shape)
    dims2 = V.ndim == 2
    return oneDim1 and dims2
def isRowVector(V):
    return V.shape[0] == 1
def isColumVector(V):
    return V.shape[1] == 1
def checkSquare(M):
    if isSquare(M) is not True:
        raise ValueError('Not square matrix')
def isSquare(M):
    return all(len(row) == len(M) for row in M)
def setTriU(M, k=0):
    checkSquare(M)
    n = len(M)
    U = np.copy(M)
    for j in range(min(n, n+k-1)):
        for i in range(max(0, j-k+1), n):
            U[i,j] = Fraction(0)
    return U
def setTriL(M, k=0):
    checkSquare(M)
    n = len(M)
    L = np.copy(M)
    for j in range(min(0, k+2), n):
        for i in range(min(j-k, n)):
            L[i,j] = Fraction(0)
    return L
def setUnitDiag(M):
    checkSquare(M)
    n = len(M)
    D = np.copy(M)
    for i in range(n):
        D[i,i] = Fraction(1)
    return D
def isTriU(M, k=0):
    checkSquare(M)
    n = len(M)
    for j in range(min(n, n+k-1)):
        for i in range(max(0, j-k+1), n):
            if M[i,j] != 0:
                return False
    return True
def isTriL(M, k=0):
    checkSquare(M)
    n = len(M)
    for j in range(min(0, k+2), n):
        for i in range(min(j-k, n)):
            if M[i,j] != 0:
                return False
    return True
def naivesubL(A, b):
    n = len(A)
    x = np.copy(b)
    for j in range(n):
        x[j] = b[j]
        xj = x[j]
        for i in range(j+1,n):
            b[i] -= A[i,j]*xj
    return x
def naivesubU(A, b):
    n = len(A)
    x = b
    for j in reversed(range(n)):
        x[j] = b[j] / A[j,j]
        xj = x[j]
        for i in reversed(range(0,j)):
            b[i] -= A[i,j]*xj
    return x
def unsafeCopyTo(dest, destI, src, srcI, N):
    for n in range(N):
        dest.flat[destI+n] = src.flat[srcI+n]