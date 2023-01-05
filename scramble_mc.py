def locate_keys(key, string):
    L = []
    x = 0
    while len(string)-x>=len(key):
        lower = string[:x]
        upper = string[x:]
        if upper.find(key) !=-1:
            L.append(upper.find(key)+len(lower))
        else:
            return L
        x = len(string[:L[-1]+len(key)])
def key_lines(key, string):
    L = locate_keys(key,string)
    lines = []
    for i in range(len(L)-1):
        lines.append(string[L[i]:L[i+1]-1])
    lines.append(string[L[-1]:])
    return lines




