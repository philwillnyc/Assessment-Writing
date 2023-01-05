import random
import sympy
from sympy.abc import x,y

#returns a list that begins with the linear and constant coefficients for a monic 
#quadratic, factorable over the integers, and ends with the solutions themselves.

def monic_integer_solution_quadratic(lower = -5, upper = 5):
    r = random.randint(lower,upper)
    s = random.randint(lower,upper)
    b = r+s
    c = r*s
    if b < 0:
        B = "-" + str(-b) +"x"
    elif b == 0: 
        B = ""
    elif b == 1:
        B = "+x"
    elif b > 1:
        B = "+" + str(b) +"x" 

    if c < 0:
        C = "-" + str(-c)
    elif c == 0: 
        C = ""
    elif c > 0:
        C = "+" + str(c)
    return [B,C,r,s]

def random_integer_polynomial(degree, lower = -9, upper = 9):
    coefficients = [random.randint(lower, upper) for i in range(degree+1)]
    exponents = [i for i in range(degree+1)]
    terms = [coefficients[i]*x**exponents[i] for i in range(degree+1)]
    poly = 0
    for i in range(degree+1):
        poly+=terms[i]
    return poly

def random_integer_two_variable_polynomial(degree, degree_min = 0, max_terms = None, lower = -9, upper = 9):
    xs = [x**i for i in range(degree + 1)]
    ys = [y**i for i in range(degree + 1)]
    all_terms = [xt*yt for xt in xs for yt in ys if sympy.total_degree(xt*yt)<= degree and sympy.total_degree(xt*yt)>= degree_min]
    if max_terms == None:
        terms = all_terms
    else:
        terms = random.choices(all_terms, k = max_terms+1)
    poly = 0
    for term in terms:
        poly+=random.randint(lower, upper)*term
    return poly

