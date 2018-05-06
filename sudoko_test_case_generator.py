

import sys

import time
import logging
import numpy as np

from random import *

from optparse import OptionParser

#Output file name
outputfile = None
samoutfile = None

#output file handle
of, sf = None, None

def wrongparam():
    print('Wrong parameters usage!!!!!')
    print('python <filename> <seperate0,1> <level 1-easy, 2-medium, 3-hard> '
          '<count> <output file name> <sample output file)')
    print("\nExiting ------------")
    sys.exit(0)

seed1 = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
]

def swapcol(mat, i, j):
    if(i != j):
        for n in range(0, 9):
            a = mat[n][i]
            mat[n][i] = mat[n][j]
            mat[n][j] = a
    return mat

def doswapcol(mat):
    for k in range(0, 10):
        col1 = randint(0, 2)
        col2 = randint(0, 2)
        mat = swapcol(mat, col1, col2)
        col1 = randint(3, 5)
        col2 = randint(3, 5)
        mat = swapcol(mat, col1, col2)
        col1 = randint(6, 8)
        col2 = randint(6, 8)
        mat = swapcol(mat, col1, col2)
    return mat

def swaprow(mat, row1, row2):
    if (row1 != row2):
        for n in range(0, 9):
            a = mat[row1][n]
            mat[row1][n] = mat[row2][n]
            mat[row2][n] = a
    return mat

def doswaprow(mat):
    for k in range(0, 10):
        row1 = randint(0, 2)
        row2 = randint(0, 2)
        mat = swaprow(mat, row1, row2)
        row1 = randint(3, 5)
        row2 = randint(3, 5)
        mat = swaprow(mat, row1, row2)
        row1 = randint(6, 8)
        row2 = randint(6, 8)
        mat = swaprow(mat, row1, row2)
    return mat

def removecell(matinput, removecellcount):
    mat = [x[:] for x in matinput]
    i = 0
    while i < removecellcount:
        row = randint(0, 8)
        col = randint(0, 8)
        if(mat[row][col] != 0):
            i = i + 1
            mat[row][col] = 0
    return mat

def getstring(mat):
    st = ""
    for i in range(0, 9):
        for j in range(0, 9):
            if (mat[i][j] == 0):
                st = st + "."
            else:
                st = st + str(mat[i][j])
    return st

def generatorSudokuInput(level):
    curseed = [row[:] for row in seed1]
    curseed = doswapcol(curseed)
    curseed = doswaprow(curseed)

    if (level == 1):
        print("Sudoko Easy Input")
        removecellcount = 81 - 50
    elif (level == 2):
        print("Sudoko Medium Input")
        removecellcount = 81 - 40
    else:  # if (level == 3):
        print("Sudoko Hard Input")
        removecellcount = 81 - 30

    sudokoinput = removecell(curseed, removecellcount)

    st = getstring(sudokoinput)

    print(st)
    return st

if __name__ == '__main__':
#def main():
    #generatorSudokuInput(1)
    #generatorSudokuInput(2)
    #generatorSudokuInput(3)

    #sys.exit(0)

    ans = ""
    #input parsing
    #print('python <filename> <seperate0,1> <level 1-easy, 2-medium, 3-hard> '
    #     '<count> <output file name> <sample output file)')
    if len(sys.argv) >= 6:
        sep = int(sys.argv[1])
        level = int(sys.argv[2])
        count = int(sys.argv[3])
        outputfile = sys.argv[4]
        samoutfile = sys.argv[5]
    else:
        wrongparam()

    print("Output file: ", outputfile)

    try:
        of = open(outputfile, 'w')
        sf = open(samoutfile, 'w')
    except IOError:
        print("Output file: Not able to create output files")
        of.close()
        sf.close()
        sys.exit(0)

    if(sep == 1):
        print("Single test case ")
        curseed = [row[:] for row in seed1]
        for t in range(0, 3):
            # do column swap
            curseed = doswapcol(curseed)
            # do row swap
            curseed = doswaprow(curseed)

        if (level == 1):
            removecellcount = 81 - 50
        elif (level == 2):
            removecellcount = 81 - 40
        else:  # if (level == 3):
            removecellcount = 81 - 30

        sudokoinput = removecell(curseed, removecellcount)

        sf.write("Solved output")
        sf.write("\n")
        for i in range(0, 9):
            print(sudokoinput[i])
            sf.write(str(curseed[i]))
            sf.write("\n")

        st = getstring(sudokoinput)

        print(st)
        of.write(st)
        of.write("\n")

    else:
        print("Multiple test case ")

        for x in range(0, count*3):
            curseed = [row[:] for row in seed1]

            for t in range(0, 3):
                # do column swap
                curseed = doswapcol(curseed)
                #do row swap
                curseed = doswaprow(curseed)
            #shuffle(curseed)

            removecellcount = 40
            if(x >= 0 and x < count):
                removecellcount = 81 - 36
            elif(x >= count and x < count *2):
                removecellcount = 81 - 30
            else: #if (level == 3):
                removecellcount = 81 - 27

            sudokoinput = removecell(curseed, removecellcount)

            sf.write("Solved output = ")
            sf.write(str(x+1))
            sf.write("\n")
            print("Input = ", x + 1)
            for i in range(0, 9):
                print(sudokoinput[i])
                sf.write(str(curseed[i]))
                sf.write("\n")

            st = getstring(sudokoinput)

            print(st)
            of.write(st)
            of.write("\n")

    of.close()
    sf.close()





