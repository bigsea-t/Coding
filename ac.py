"""
Arithmetic Coding 

************************************************************************

    File    : arcode.py
    Purpose : This file implement simple functions for compressing 
              string using the arithmetic coding algorithm.
    Author  : Taikai Takeda
    Date    : Nov 18, 2014
    Env     : Python 3.3.5

************************************************************************


Copyright (C) 2014
      Taikai Takeda(297.1951@gmail.com)

"""

def cal_q(p):
    '''
    Calculate cumulative probability from probability list
    p: probability list

    ret: cumulative probability list
    '''
    q = []
    sum = 0
    for val in p:
        q.append(sum)
        sum += val
    return q

def prod(lst, range = None):
    '''
    Production of element in list in range
    range:tuple(start,end) default: all of elements

    ret: production result
    '''
    if range == None:
        range = (0,len(lst))
    elif range[0] > range[1]:
        raise
    pr = 1
    for val in lst[range[0]:range[1]]:
        pr *= val
    return pr

def sum(lst, range):
    '''
    Summation of element in list in range
    range:tuple(start,end) default all of elements

    ret: summation result
    '''
    if range[0] > range[1]:
        raise
    elif range == None:
        range = (0,len(lst))

    sm = 0
    for val in lst[range[0]:range[1]]:
        sm += val
    return sm

def cal_u(px,qx):
    '''
    Calculate  u from px,qx lists
    px: probability list of simbols to encode
    qx: cumulative probability list of simbols to encode

    ret: u
    '''
    u = 0
    for i in range(0,len(px)):
        u += prod(px,(0,i))*qx[i]
    return u

def cal_v(px,qx):
    '''
    Calculate  v from px,qx lists
    px: probability list of simbols to encode
    qx: cumulative probability list of simbols to encode

    ret:v
    '''
    return prod(px) + cal_u(px,qx)

def orderL(num):
    '''
    order L 
    2^-L < num < 2^-(L-1)

    ret:num
    '''
    if num <= 0 or num > 1:
        raise
    th    = 1.0
    order = 0
    while True:
        if(num>th):
            return order
        order += 1
        th    /= 2.0

def seekPos(uv, pos = 0.5, posDlt = 0.25):
    '''
    seek the point between u and v, which is
    represented as 1/2^L(minimum L). Used binary search for efficiency.

    uv: (u,v)
    pos: start seeking position in (0,1)
    posDlt: used for default seeking distance

    ret: pos between [u,v)
    '''
    if pos < uv[0] :
        return seekPos(uv, pos+posDlt, posDlt/2.0)
    elif pos >= uv[1] :
        return seekPos(uv, pos-posDlt, posDlt/2.0)
    elif uv[0] <= pos < uv[1]:
        return pos
    else:
        raise
            


def seekLM(uv, L = 1, pos = None):
    '''
    seek L and M
    There are three patterns
    remember pos is in [u,v)
    1. pos - 2**(-L) is in [u,v)
    2. pos + 2**(-L)  is in [u,v)
    3. other -> L = L/2 and seek again

    caution: DO NOT change the order of these if-else statements
    M need to be the 'Minimum' number of some representitives

    L : start L 
    uv: (u,v)
    pos: start seeking position in (0,1)
    posDlt: used for default seeking distance

    ret:(L,M)
    '''
    if pos == None:
        print(uv)
        pos = seekPos(uv)

    print(pos)

    if pos-2**(-L) >= uv[0]:
        M = round(pos * 2**L -1)
        return (L,M)
    elif pos+2**(-L) < uv[1]:
        M = round(pos * 2**L)
        return (L,M)
    else:
        return seekLM(uv, L+1, pos)

def encode(simbols, p, q, simbolList, prnt = False):
    '''
    encode simbolList
    sibmols: simbol data
    p: probability list of simbol data
    q: cumulative probability list of simbol data

    ret: encoded string
    '''
    px = []
    qx = []

    for val in simbolList:
        px.append(p[simbols.index(val)])
        qx.append(q[simbols.index(val)])

    u = cal_u(px,qx)
    v = cal_v(px,qx)

    L_0 = orderL(v-u)

    L,M = seekLM((u,v), L = L_0)

    if prnt:
        print('u:',u)
        print('v:',v)
        print('L:',L)
        print('M:',M)

    return format(M, 'b').zfill(L)


# ----------------------------------
#              Test
# ----------------------------------

simbol = ['A','B','C','D','E','H']
p      = [0.10,0.30,0.25,0.15,0.10,0.10]
q      = cal_q(p)
simbolList = list("BDC")

print('endcode(BCD):',encode(simbol, p, q, simbolList, prnt=True))

simbol = ['1','2','3','4','5','6']
p      = [3/16,1/16,3/16,2/16,4/16,3/16]
q      = cal_q(p)
simbolList = list("6151345565246313")

print("endcode(6151345565246313):",encode(simbol, p, q, simbolList, prnt=True))
