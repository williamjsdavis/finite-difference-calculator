import numpy as _np
from fractions import Fraction as _Fraction
import fractions as _fractions
from operator import matmul as _matmul
import utils as _utils
class RationalMatrix:
    # Only supports square matrices
    def __init__(self, intMatrix):
        _utils.checkSquare(intMatrix)
        self.value = intMatrix + _Fraction()
        self.length = len(intMatrix)
    def __add__(self, other):
        T = type(other)
        if T is RationalMatrix:
            out = self.value + other.value
        elif T is float:
            out = self.value + _Fraction(other)
        else:
            out = self.value + other
        return RationalMatrix(out)
    def __radd__(self, other):
        T = type(other)
        if T is int or T is _Fraction or T is RationalMatrix:
            outRa = self + other
        elif T is float:
            out = _Fraction(other) + self.value
            outRa = RationalMatrix(out)
        else:
            out = other + self.value
            outRa = RationalMatrix(out)
        return outRa
    def __mul__(self, other):
        T = type(other)
        if T is float:
            out = self.value * _Fraction(other)
        else:
            out = self.value * other
        return RationalMatrix(out)
    def __rmul__(self, other):
        T = type(other)
        if T is int or T is _Fraction or T is float:
            outRa = self * other
        else:
            out = other * self.value
            outRa = RationalMatrix(out)
        return outRa
    def __matmul__(self, other):
        T = type(other)
        if T is RationalVector:
            out = _matmul(self.value, other.value)
            outRa =  RationalVector(out)
        elif T is RationalMatrix:
            out = _matmul(self.value, other.value)
            outRa = RationalMatrix(out)
        else:
            out = _matmul(self.value, other)
            if _utils.isSquare(out):
                outRa = RationalMatrix(out)
            elif _utils.isVector(out):
                outRa = RationalVector(out)
        return outRa
    def __rmatmul__(self, other):
        T = type(other)
        if T is RationalVector:
            out = _matmul(other.value, self.value)
            outRa = RationalVector(out)
        elif T is RationalMatrix:
            out = _matmul(other.value, self.value)
            outRa = RationalMatrix(out)
        else:
            out = _matmul(other, self.value)
            if _utils.isSquare(out):
                outRa = RationalMatrix(out)
            elif _utils.isVector(out):
                outRa = RationalVector(out)
        return outRa
    def __str__(self):
        max_chars = max([len(str(item)) for item in self.value.flat])
        formStr = '%0' + str(max_chars) + 's'
        strFun = lambda x: formStr % str(x)
        return '['+',\n '.join('['+', '.join(map(strFun, row))+
                             ']' for row in self.value)+']'
class RationalVector:
    def __init__(self, intVector):
        _utils.checkVector(intVector)
        self.value = intVector + _Fraction()
        self.length = len(self.value)
    def __add__(self, other):
        T = type(other)
        if T is int or T is _Fraction:
            out = self.value + other
            outRa = RationalVector(out)
        elif T is float:
            out = self.value + _Fraction(other)
            outRa = RationalVector(out)
        else:
            if T is RationalVector:
                out = self.value + other.value
            else:
                out = self.value + other
            if _utils.isVector(out):
                outRa = RationalVector(out)
            elif _utils.isSquare(out):
                outRa = RationalMatrix(out)
            else:
                raise ValueError('Dimension mismatch.')
        return outRa
    def __radd__(self, other):
        T = type(other)
        if T is int or T is _Fraction or T is RationalVector:
            outRa = self + other
        elif T is float:
            out = _Fraction(other) + self.value
            outRa = RationalVector(out)
        else:
            out = other + self.value
            outRa = RationalVector(out)
        return outRa
    def __mul__(self, other):
        T = type(other)
        if T is float:
            out = self.value * _Fraction(other)
        else:
            out = self.value * other
        return RationalVector(out)
    def __rmul__(self, other):
        T = type(other)
        if T is int or T is _Fraction or T is float:
            outRa = self * other
        else:
            out = other * self.value
            outRa = RationalVector(out)
        return outRa
    def __matmul__(self, other):
        T = type(other)
        if T is RationalVector or T is RationalMatrix:
            out = _matmul(self.value, other.value)
            if _utils.isColumVector(self.value):
                outRa = RationalMatrix(out)
            else:
                outRa = RationalVector(out)
        else:
            out = _matmul(self.value, other)
            if _utils.isSquare(out):
                outRa = RationalMatrix(out)
            elif _utils.isVector(out):
                outRa = RationalVector(out)
        return outRa
    def __rmatmul__(self, other):
        T = type(other)
        if T is RationalVector or T is RationalMatrix:
            out = _matmul(self.value, other.value)
            if _utils.isColumVector(self.value):
                outRa = RationalVector(out)
            else:
                outRa = RationalMatrix(out)
        else:
            out = _matmul(other, self.value)
            if _utils.isSquare(out):
                outRa = RationalMatrix(out)
            elif _utils.isVector(out):
                outRa = RationalVector(out)
        return outRa
    def __str__(self):
        max_chars = max([len(str(item)) for item in self.value.flat])
        formStr = '%0' + str(max_chars) + 's'
        strFun = lambda x: formStr % str(x)
        return '['+',\n '.join('['+', '.join(map(strFun, row))+
                             ']' for row in self.value)+']'
def inv(inRM):
    M = inRM.value
    A, ipiv = _LUrational(M)
    Mi = _invLU(A, ipiv)
    return RationalMatrix(Mi)
def identity(n):
    return RationalMatrix(_np.identity(n).astype(int))
def lu(inRM):
    M = inRM.value
    A, ipiv = _LUrational(M)
    L = _utils.setUnitDiag(_utils.setTriL(A))
    U = _utils.setTriU(A)
    B = _applyIpivRows(A, ipiv)
    return RationalMatrix(L), RationalMatrix(U), RationalMatrix(B)
def _LUrational(M):
    _utils.checkSquare(M)
    A = _np.copy(M)
    n = len(A)
    ipiv = _np.zeros(n, dtype=int)
    info = 0
    for k in range(n):
        kp = k
        amax = _Fraction(0,1)
        for i in range(k, n):
            absi = abs(A[i,k])
            if absi > amax:
                kp = i
                amax = absi
        ipiv[k] = kp
        if A[kp,k] != 0:
            if k != kp:
                # Interchange
                for i in range(n):
                    tmp = A[k,i]
                    A[k,i] = A[kp,i]
                    A[kp,i] = tmp
            # Scale first column
            Akkinv = _reciprocal(A[k,k])
            for i in range(k+1,n):
                A[i,k] *= Akkinv
        elif info == 0:
            info = k
        for j in range(k+1, n):
            for i in range(k+1, n):
                A[i,j] -= A[i,k]*A[k,j]
    return A, ipiv
def _applyIpivRows(A, ipiv):
    n = len(A)
    B = _np.identity(n).astype(int) + _Fraction()
    for i, j in enumerate(ipiv):
        if i != j:
            for col in range(n):
                B[i,col], B[j,col] = B[j,col], B[i,col]
    return B
def _reciprocal(A):
    return _Fraction(A._denominator, A._numerator)
def _ldivLU(A, B, Mtype):
    _utils.checkSquare(A)
    nA = len(A)
    tmp = _np.zeros(nA).astype(int) + _Fraction()
    nB = len(B)
    for i in range(nB):
        _utils.unsafeCopyTo(tmp, 0, B, i*nB, nB)
        if Mtype is 'L':
            _utils.naivesubL(A, tmp)
        elif Mtype is 'U':
            _utils.naivesubU(A, tmp)
        _utils.unsafeCopyTo(B, i*nB, tmp, 0, nB)
    return B.transpose()
def _invLU(M, ipiv):
    B = _applyIpivRows(M, ipiv)
    L = _utils.setUnitDiag(_utils.setTriL(M))
    U = _utils.setTriU(M)
    tmp = _ldivLU(L, B.transpose(), 'L')
    return _ldivLU(U, tmp.transpose(), 'U')
