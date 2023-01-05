from array_builder import *
import numpy as np
import random
#Game Theory: make a strictly determined game matrix (one saddle point selected, more can occur by chance):

def strictly_determined(rows=4, columns = 4, low =-2, high= 15, var = 4):
    #initialize matrix:
    M = rand_int_matrix(rows, columns, low, high)
    #select a saddle point:
    saddle_row = random.randint(0, rows-1)
    saddle_column = random.randint(0, columns-1)
    M[saddle_row, saddle_column] = random.randint(low, high)
    #fill saddle row:
    for j in range(np.size(M,axis = 1)):
        if j == saddle_column:
            pass
        else:
             M[saddle_row,j] = random.randint(M[saddle_row, saddle_column], M[saddle_row, saddle_column]+var)
    #fill saddle column:
    for row in range(np.size(M, axis = 0)):
        if M[row, saddle_column] == M[saddle_row, saddle_column]:
            pass
        else: M[row,saddle_column] = random.randint(M[saddle_row, saddle_column]-var, M[saddle_row,saddle_column])
    return M
