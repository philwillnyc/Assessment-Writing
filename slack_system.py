#This script is designed to fill in the table for the linear programming quiz problem. It has not been used yet!
import numpy as np 
import array_builder as AB
import row_reduction as RR
import random

M = AB.int_sol_matrix(2, low = 1, zeros = True)
ME = np.append(M, [[1,0,0],[0,1,0]], axis = 0)
T = AB.tex_inequality_system(ME[:,:2],ME[:,2:],variables = ['x_1','x_2'], symbollist = [r'\leq',r'\leq',r'\geq',r'\geq'] )
ox = random.randint(4,8)
oy = 5*random.randint(2,10)
M1 = np.append(M[:,:-1], [[1,0],[0,1]],1)
slack_system = np.append(M1, M[:,-1:],1)
M01 = np.delete(slack_system,(0,1), axis = 1)
S01 = np.matmul(np.linalg.inv(M01[:,:-1]), M01[:,-1:])
M02 = np.delete(slack_system,(0,2), axis = 1)
S02 = np.matmul(np.linalg.inv(M02[:,:-1]), M02[:,-1:])
M03 = np.delete(slack_system,(0,3), axis = 1)
S03 = np.matmul(np.linalg.inv(M03[:,:-1]), M03[:,-1:])
M12 = np.delete(slack_system,(1,2), axis = 1)
S12 = np.matmul(np.linalg.inv(M12[:,:-1]), M12[:,-1:])
M13 = np.delete(slack_system,(1,3), axis = 1)
S13 = np.matmul(np.linalg.inv(M13[:,:-1]), M13[:,-1:])
M23 = np.delete(slack_system,(2,3), axis = 1)
S23 = np.matmul(np.linalg.inv(M23[:,:-1]), M23[:,-1:])


