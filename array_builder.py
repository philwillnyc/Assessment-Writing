import numpy
import numpy as np
import random
from sympy import Rational
import row_reduction as RR


def rand_matrix(rows, columns, low, high, rounding):
    M = high*numpy.random.rand(rows,columns)+low
    return numpy.around(M,rounding)

def rand_int_matrix(rows, columns, low, high):
    return numpy.random.randint(low, high = high + 1, size = (rows,columns))

def rank_given_int_matrix(rows,columns, rank, low, high):
    pass
    
#generate a random invertible 2 by 2 integer matrix; by default, no zeros.
#the size factor will adjust the complexity of the matrix. 

def sl2z(size_factor, no_zeros = True):
    G1 = [[1,1],[0,1]]
    G2 = [[0, -1],[1,0]]
    L = [G1, G2, np.linalg.inv(G1), np.linalg.inv(G2)]
    M = [[1,0],[0,1]]
    if no_zeros == False:
        for i in range(0, size_factor):
            M = np.matmul(M, random.choice(L))
        return M
    else:
        while M[0][0]*M[0][1]*M[1][0]*M[1][1] == 0:
            for i in range(0, size_factor):
                M = np.matmul(M, random.choice(L))
        return M

def int_sol_matrix(dim, low = -5, high = 5, zeros = True):
    n=0
    while n == 0:
        M = rand_int_matrix(dim,dim,low,high)
        V = rand_int_matrix(dim,1,low,high)
        if zeros == True:
            n = np.prod(M)
        else:
            n = 1
        if np.linalg.det(M) == 0:
            n = 0
    return np.append(M, np.matmul(M,V), axis = 1)


def int_invertable_matrix(dim, low = -5, high = 5, zeros = True, detone = False):
    n=0
    while n == 0:
        M = rand_int_matrix(dim,dim,low,high)
        if zeros == True:
            n = np.prod(M)
        else:
            n = 1
        if np.linalg.det(M) == 0:
            n = 0
        if detone == True and np.linalg.det(M) != 1:
            n = 0
    return M
        
#Generate latex code for a given matrix

def prep_matrix(array):
    array = np.array(array, dtype = 'O')
    RR.fractionize(array)
    RR.tex_fractions_array(array)
    return array

def prep_decimal_matrix(array):
    pass

#admittedly this function is a disaster and should be rewritten more simply.
#The two cases of wanting fraction matrices and decimal matrices were not properly anticipated.
def tex_matrix(array, augmented = False, decimal = False):
    if decimal == False:
        array = prep_matrix(array)
    rows = numpy.size(array,0)
    columns = numpy.size(array,1)
    if augmented == False:
        latex_code = r"\begin{bmatrix}"+ "\n"
    if augmented == True:
        aug = '['
        for i in range(columns-1):
            aug += 'c'
        aug+='|c]'
        latex_code = r"\begin{bmatrix}" + aug + "\n"
    for i in range(0, rows-1):
        for j in range (0, columns-1):
            if decimal == True and array[i,j]==int(array[i,j]):
                latex_code += str(int(array[i, j])) + " & "
            else:
                latex_code += str(array[i, j]) + " & "    
        if decimal == True and array[i,columns-1]== int(array[i,columns-1]):
            latex_code += str(int(array[i,columns-1])) + r" \\" +"\n"
        else:
            latex_code += str(array[i,columns-1]) + r" \\" +"\n"
    for j in range (0, columns-1):
        if decimal == True and array[rows-1, j]==int(array[rows-1,j]):
            latex_code += str(int(array[rows-1, j])) + " & "
        else:
            latex_code += str(array[rows-1, j]) + " & "
    if decimal == True and array[rows-1,columns-1] == int(array[rows-1,columns-1]):
        latex_code += str(int(array[rows-1,columns-1])) +"\n" + r"\end{bmatrix}"
    else:
        latex_code += str(array[rows-1,columns-1]) +"\n" + r"\end{bmatrix}"
    return latex_code

#Generate latex code for a given table
def tex_table(array):
    rows = numpy.size(array,0)
    columns = numpy.size(array,1)
    c = '|' 
    for i in range(0,columns):
        c +='c|'
    latex_code = r'\begin{center}' +'\n' + r'\begin{tabular}{' + c + '} \n' + r'\hline' + '\n'
    for i in range(0, rows-1):
        for j in range (0, columns-1):
            latex_code += str(array[i, j]) + " & "
        latex_code += str(array[i,columns-1]) + r" \\" +"\n" +r"\hline" + "\n"
    for j in range (0, columns-1):
        latex_code += str(array[rows-1, j]) + " & "
    latex_code += str(array[rows-1,columns-1])+ r" \\" +"\n" + r"\hline" + "\n" + r"\end{tabular}" + "\n" + r"\end{center}"
    return latex_code

def s_term(array, i, j,variables):
    N = array[i,j]
    if variables == []:
        C = "x_{" + str(int(j+1))+"}"
    else:
        C = variables[j]
    if N - int(N) == 0:
        N = int(N)
    if not(abs(array[i,j]) == 1):
        C = str(abs(N))+C
    if np.sign(N) == -1:
        C = "-" + C
    elif np.sign(N) == 1:
        C = "+" + C
    elif np.sign(N) == 0:
        C = ""
    return C

def s_row(array,i,variables):
    R = ""
    for j in range(0, np.size(array,1)):
        R = R + s_term(array,i,j,variables)
    if R[0] == "+":
        R = R[1:]
    return R

def se_row(array, vector, i, variables, symbol = '='):
    if type(vector[i,0]) == numpy.str_:
        S = vector[i,0]
    elif vector[i,0] - int(vector[i,0]) == 0:
        S = str(int(vector[i,0]))
    else:
        S = str(vector[i,0])                
    return s_row(array,i,variables)+ " &{0} ".format(symbol) + S + r" \\" + "\n"
    
                     
def tex_system(array, vector, variables = [], symbol = '='):
    if type(variables) == list and (len(variables) == np.size(array, 1) or len(variables) == 0):
        pass
    else:
        raise Exception('Custom variables must be given as a list of length ' + str(np.size(array,1)))
        
    T = r'\begin{align*}'+'\n'
    for i in range(0, np.size(array,0)):
        T += se_row(array,vector,i,variables, symbol = symbol)
    return T[:-3] + '\n' + r'\end{align*}'

def tex_inequality_system(array, vector, variables = [], symbollist = []):
    if symbollist == []:
       symbollist = [r'\leq' for i in range(np.size(array,0))]        
    T = r'\begin{align*}'+'\n'
    for i in range(0, np.size(array,0)):
        T += se_row(array,vector,i,variables, symbol = symbollist[i])
    return T[:-3] + '\n' + r'\end{align*}'

#Creates latex code for a system of equations or inequalities with integer solutions:

def int_sol_system(dim, low = -5, high = 5, zeros = True, variables = [], symbol = '='):
    n=0
    while n == 0:
        M = rand_int_matrix(dim,dim,low,high)
        V = rand_int_matrix(dim,1,low,high)
        if zeros == False:
            n = np.prod(M)
        else:
            n = 1
    return tex_system(M,np.matmul(M,V), variables, symbol = symbol)

def sl2z_system(srange, variables = []):
    V = rand_int_matrix(2,1,-srange, srange)
    M = sl2z(2*srange)
    return tex_system(M,np.matmul(M,V), variables)

def nice_io_matrix():
    condition = False
    R = random.choice([80,90,95])
    while condition == False:
    
        a = random.randint(1,R-1)
        d = R-a
        factors = []
        for i in range(1,a*d+1):
            if a*d % i == 0:
                factors.append(i)
        b = random.choice(factors)
        c = a*d/b
        if a+c < 100 and b+d < 100 and round(a,5) != round(b,5):
            condition = True
    return np.array([[a/100,b/100],[c/100,d/100]])

def three_inequalities_two_unknowns(low, high):
    pass

    
    
if __name__ == '__main__':
    A = np.array([[1.5, 1.99, 8], [7, 3, 1.111]])
    print(tex_matrix(A))
        



#matrix = numpy.random.randint(-100, high=101, size = (5,4))
#numpy.random.rand(3,4)

      

