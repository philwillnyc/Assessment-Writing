import numpy as np
import array_builder as AB
from fractions import Fraction
from sympy import Rational
import random
#The Matrix class features an array and lists to record all of the steps.
class Matrix(np.ndarray):
    def __init__(self, shape, dtype = 'O'):
        super().__init__()
        self.steps = []
        self.step_description = []

#Makes a matrix:
def matrix(twodarray):
    N = np.array(twodarray, dtype = 'O')
    M = Matrix((np.size(N,0),np.size(N,1)), dtype = 'O')
    for i in range(np.size(N,0)):
        for j in range(np.size(N,1)):
            M[i,j] = N[i,j]
    M.steps.append(np.copy(N))
    return M

#This function ensures the entries are sympy Rational, which the algorithm requires:
def fractionize(M):
    for i in range(np.size(M,0)):
        for j in range(np.size(M,1)):
            M[i,j] = Rational(M[i,j]).limit_denominator(10**12)

#Functions for testing if a matrix is an integer matrix:
def is_integer(x):
    return np.equal(np.mod(x,1),0)

def is_integer_matrix(M):
    return is_integer(M).all()

#The matrix row operations:
def swap(array, i, j):
    if i == j:
        pass
    I = list(array[i])
    J = list(array[j])
    array[i] = J
    array[j] = I
    if i != j and type(array) == Matrix:
        array.steps.append(np.copy(array))
        array.step_description.append('swap row ' + str(i+1) + ' and row ' + str(j+1) + ':')
    
def mult(array, i, scalar):
    array[i] = scalar*array[i]
    if scalar != 1 and type(array) == Matrix:
        array.steps.append(np.copy(array))
        array.step_description.append('Multiply row ' + str(i+1) +
                                      ' by $' + str(tex_fraction(scalar)) + '$:')
    
def add(array, s_row, factor, t_row):
    array[t_row] = factor*array[s_row] + array[t_row]
    if factor != 0 and type(array) == Matrix:
        array.steps.append(np.copy(array))
        if factor != 1:
            array.step_description.append('Add $' + str(tex_fraction(factor))
                                          + '$ times row ' + str(s_row+1) + ' to row ' + str(t_row+1) + ':')
        if factor == 1:
            array.step_description.append('Add row ' + str(s_row+1) + ' to row ' + str(t_row+1) + ':')
        
def uniformize_entry(M, i,j):
    mult(M, i, 1/M[i,j])

#GCD function for simplifying rows:

def gcd(row):
    if len(row) == 1:
        return row[0]
    a = row[0]
    for i in range(1,len(row)):
        a = np.gcd(a, row[i])
    return a

def divide_by_gcd(M, i):
    row = M[i]
    g = gcd(row)
    if g !=0:
        mult(M, i, 1/g)

#functions for clearing columns:
    
def clear_around(M, i, j):
    for k in range(i):
        add(M, i, -M[k,j]/M[i,j], k)
    for k in range(i+1, np.size(M,0)):
        add(M, i, -M[k,j]/M[i,j], k)

def eliminate_around(M,i,j):
    for k in range(i):
        if M[k,j] != 0:
            L = Rational(np.lcm(M[i,j],M[k,j]))
            if M[i,j] == -M[k,j]:
                add(M, i, 1, k)
            else:
                mult(M, k, L/M[k,j])
                add(M, i, -L/M[i,j], k)
    for k in range(i+1, np.size(M,0)):
        if M[k,j] != 0:
            L = Rational(np.lcm(M[i,j],M[k,j]))
            if  M[i,j] == -M[k,j]:
                add(M, i, 1, k)
            else:
                mult(M, k, L/M[k,j])
                add(M, i, -L/M[i,j], k)

#Functions used to tell the row reduction algorithm to determine how to proceed:         
def truncate(M, i, j):
    return M[i+1:,j+1:]

def is_not_zero_column(M, j): 
    return bool(M[:,j].any())

#These are the main row reduction algorithms:
        
def field_row_reduction(M):#performs row reduction with fractions and records steps in M.steps
    fractionize(M)
    pivot = [-1,-1] #use the pivot to determine where to truncate; initial matrix is "truncated" outside itself 
    pivotlist = []
    for j in range(np.size(M,1)):
        T = truncate(M, pivot[0], pivot[1]) #truncate at the pivot
        if is_not_zero_column(T,0) == True: #zero columns after truncating are free variables; we move on if this is the case
            if 1 in T[:,0]: #if we have a 1, use it!
                r = M[:,j].tolist().index(1,pivot[0]+1) #r will be the row we use to eliminate
            else:
                B = [bool(entry) for entry in M[:,j].tolist()] # if we don't have a 1, we mark the rows with nonzero entries in jth column
                r = B.index(True, pivot[0] + 1) #the first of these will be used for elimination
            swap(M, pivot[0]+1,r) #we move the eliminating row to one below the pivot
            clear_around(M,pivot[0]+1, j) #eliminate
            pivot[0] += 1 #adjust the pivot
            pivot[1] = j
            pivotlist.append(list(pivot))#keep track of pivot; we will have to uniformize each row based on the pivot
        else:
            pivot[1] = j
    for j in range(np.size(M,0)):
        if any(M[j]):
            uniformize_entry(M,pivotlist[j][0], pivotlist[j][1])
    for j in range(np.size(M,0)): #move zeros to bottom
        if not any(M[j]) and j < np.size(M,0)-1:
            for k in range(j+1, np.size(M,0)):
                r = 0
                swap(M, k-1, k)

def integer_row_reduction(M): #similar to Field RR but avoids dividing
    fractionize(M)
    pivot = [-1,-1]
    pivotlist = []
    for j in range(np.size(M,1)):
        T = truncate(M, pivot[0], pivot[1])
        if is_not_zero_column(T,0) == True:
            lcms = {}
            for i in range(len(T[:,0])):
                override = False
                a = T[:,0][i]
                if a == 0: # skip over any zero entry
                    continue
                if all([not(b % a) for b in T[:,0]]): #if everything is a multiple, use the row
                    r = i + pivot[0] + 1
                    override = True
                    break
                else:
                    lcms[max([abs(np.lcm(a,b)) for b in T[:,0]])] = i #record the max that stuff would have to be scaled to
            if override == False:
                r = lcms[min(lcms)] + pivot[0] + 1
            swap(M, pivot[0]+1,r) #we move the eliminating row to one below the pivot         
            eliminate_around(M,pivot[0]+1, j) #eliminate
            pivot[0] += 1 #adjust the pivot
            pivot[1] = j
            pivotlist.append(pivot.copy())
        else:
            pivot[1] = j
            #keep track of pivot; we will have to uniformize each row based on the pivot
    for j in range(np.size(M,0)):
        if any(M[j]):
            uniformize_entry(M,pivotlist[j][0], pivotlist[j][1])
    for j in range(np.size(M,0)): #move zeros to bottom
        if not any(M[j]) and j < np.size(M,0)-1:
            for k in range(j+1, np.size(M,0)):
                r = 0
                swap(M, k-1, k)
                    
def row_reduce(array):
    if is_integer_matrix(array):
        integer_row_reduction(array)
    else:
        field_row_reduction(array)

#Functions for building latex output based on the recorded steps:
        
def tex_fraction(f):
    if is_integer(f) == True:
        return f
    if abs(f) == f:
        return r'\frac{' + str(f.p) + '}{' + str(f.q) +'}'
    else:
        return r'-\frac{' + str(abs(f.p)) + '}{' + str(abs(f.q)) +'}'

def tex_fractions_array(array):
    for i in range(np.size(array, 0)):
        for j in range(np.size(array,1)):
            array[i,j] = tex_fraction(array[i,j])
                
def tex_matrix_steps(matrix, describe = True, augmented = False):
    L = matrix.steps.copy()
    S = 'We will row reduce the following matrix: \n \n'
    for i in range(len(matrix.steps)):
        tex_fractions_array(L[i])
        if describe == True and i !=0:
            S += matrix.step_description[i-1] + '\n\n'
        S += '$' + AB.tex_matrix(L[i], augmented = augmented) + '$ \n\n'
    return S

#given a 2d numpy array, will return the tex for row reduction of the corresponding matrix
def tex_row_reduce(array, augmented = False):
    M = matrix(array)
    row_reduce(M)
    return tex_matrix_steps(M, augmented = augmented)

def example_maker():
        for j in range(4):
            print(r'\question' + '\n\n')
            M = AB.rand_int_matrix(3, 4, -6,6)
            print(tex_row_reduce(M, augmented = True))
            print('\n \n')

if __name__ == '__main__':
    M= np.array([
                [2,4, 6, 4, 4], 
                [2, 5, 7, 6, 3], 
                [2, 3, 5, 2, 5]
                ])
    N = np.array([
                [2, 4, -10, -2],
                [3, 9, -21, 0], 
                [1, 5, -12, 1]
                ])
    P = np.array(
                [[2, 6, 15, -12],
                [4, 7, 13, -10], 
                [3, 6, 12, -9]
                ])
    R = np.array(
                [[2, -2, 4, -2], 
                [3, -3, -6, -3], 
                [-2, 3, 1, 7]
                ])
    S = np.array([[1,1,1,16], 
                 [300, 900, 1500, 19200]
                 ])
    for j in [M, N, P, R, S]:
        print(r'\question' + '\n\n')
        print(tex_row_reduce(j, augmented = True))
        print('\n \n')


    
    
    

###Functions I dind't end up using

##def lcm(number_list):
##    number_list = [value for value in number_list if value !=0]
##    if number_list == []:
##        return 1
##    if len(number_list) == 1:
##        return number_list[0]
##    a = number_list[0]
##    for i in range(1, len(number_list)):
##        a = np.lcm(a, number_list[i])
##    return a
##            

##
##def GcdMatrixRows(M): #divides all rows by their gcds
##    for i in range(np.size(M,0)):
##        if gcd(M[i]) > 1:
##            GcdMatrixRow(M, i)
##
##def lcmMatrixColumn(M, j): #scales a column to the lcm
##    number_list = [M[i,j] for i in range(np.size(M,0))]
##    for i in range(np.size(M,0)):
##        if M[i,j] != 0:
##            M[i] = lcm(number_list)/abs(M[i,j])*M[i]
##    

