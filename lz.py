"""
Lempel-Ziv Coding 

************************************************************************

    File    : lz.py
    Purpose : This file implement simple functions for compressing 
              binary string using the lz coding algorithm.
    Author  : Taikai Takeda
    Date    : Nov 19, 2014
    Env     : Python 3.3.5

************************************************************************


Copyright (C) 2014
      Taikai Takeda(297.1951@gmail.com)

"""
import math
import random
import sys

def matchIndexInDict(raw, dict_lst):
    '''
    matched value index in dict_list in maximun length.
    '''
    pat = ''
    match_idx = 0
    prev_idx  = 0
    for idx, char in enumerate(raw):
        prev_idx = match_idx 
        pat += char
        if pat in dict_lst:
            match_idx = dict_lst.index(pat)
        else:
            return prev_idx
    return prev_idx

def dictIndexToAppend(matchedIndexInDict, dictLength):
    length = math.ceil(math.log(dictLength,2))
    if length <= 0:
        return ''
    else:
        binary = format(matchedIndexInDict,'b').zfill(length)
        return binary

def encode(raw):
    # index: registered number
    # value: registered bit pattern
    dict_lst = []
    dict_lst.append("")

    coded = ''

    while len(raw)>0:
        matchedIndexInDict =  matchIndexInDict(raw, dict_lst)
        if matchedIndexInDict > 0:
            matchedLength = len(dict_lst[matchedIndexInDict])
        else:
            matchedLength = 0

        coded += dictIndexToAppend(matchedIndexInDict, len(dict_lst)) + raw[matchedLength]
        newPattern = raw[0:matchedLength+1]
        dict_lst.append(newPattern)
        raw = raw[matchedLength+1: len(raw)]

    return coded

def randomBin(length):
    bn = ''
    for i in range(0,length):
        bn += str(random.randint(0,1))
    return bn

# def randomBin(length, acm =''):
    ## python doesn't support tail recursive optimization.
    ## so, this type of recursion is not recommended
    # if length <= 0:
    #     return acm
    # else:   
    #     return randomBin(length-1, acm + str(random.randint(0,1)))

def main():
    sys.setrecursionlimit(10**5)
    raw = '110001101001011100101101110101010100110011001011'

    encoded = encode(raw)

    print('answer:',encoded)

    print('-'*30)
    print('compression test')
    print('-'*30)

    for i in range(1,10):
        raw = randomBin(10**i)
        encoded = encode(raw)
        print('length:10^{0}, encoded length: {1}, compression raito:{2}%'
            .format(i,len(encoded), round(len(encoded) / 10.0**i * 100.0,1)))



if __name__ == "__main__":
    main()


    
