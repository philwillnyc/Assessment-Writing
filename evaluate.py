#take a string and within the string take instances of \py{code}, evaluate the code, replace \py{code} with the output.
#will build it to be more general
import random
#list the indices of specified opening characters
def indices(open,string):
    i = string.find(open)
    k = len(open)
    n = 0
    L = []
    s = string
    while i != -1:
        i = s.find(open)
        if i != -1:
            n+=i+k
            L.append(n-k)
        s = string[n:]
    return L

#extract the string between the first instance of the opening characters and the close characters; 
# return a list of the inside and also with the opening and closing characters included. 
def read(string, open, close):
    o = string.find(open)+len(open)
    c = string[o:].find(close)+o
    return [string[o:c], string[o-len(open):c+len(close)]]

#make a list of outputs
def outputs(string, open, close, variables):
    L = []
    for i in indices(open,string):
        L.append(eval(read(string[i:], open, close)[0], globals(), variables))
    return L

def replacement(string, open, close, variables):
    new_string = string
    ops = outputs(string, open, close, variables)
    if ops == []:
        return new_string
    for o in ops:
        r = read(new_string, open, close)
        new_string = new_string.replace(r[1], str(o),1)
    return new_string

    

