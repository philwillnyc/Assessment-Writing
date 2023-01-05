import row_reduction as RR
import array_builder as AB
import numpy as np
import random
from sympy import Rational

def Kron(i,j):
    if i == j:
        return 1
    else:
        return 0
    
def Identity(n):
    I = np.zeros((n,n), dtype = int)
    for i in range(n):
        for j in range (n):
            I[i,j] = Kron(i,j)
    return I

def Alter(M):
    n = np.size(M,0)
    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    o = random.randint(0,1)
    if i == j:
        o = -1
    if o == 0:
        RR.swap(M, i,j)
    if o == 1:
        k = random.randint(1,3)
        s = random.choice([-1,1])
        RR.add(M, i, k*s , j)

def make_sln_matrix(n, complexity=20):
    M = Identity(n)
    RR.fractionize(M)
    for i in range(complexity):
        Alter(M)
    return M

if __name__ == '__main__':
    pass

    
print(make_sln_matrix(3,complexity =13))