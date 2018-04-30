
import getopt
import sys
import heapq
#from queue import PriorityQueue
import time
import queue
import collections

import numpy as np

from sudokuGenerator import SudokuGenerator


# few global variable used across
false = 0
true = 1

#size - is basically number of variables
size = 0

#domain - it basically the number of values(colors) possible for each variables
domain = 0

#deg - Degree of each variable as per the graph
deg = []

#variable to count the number of searches
search = 0

#Variable to count the number of prune
prune = 0

#FFunction to check if the current assignment is satisfying all the constraints,
# if then return true to indicate this is the final solution.
def checksol(mat, arr):
    for x in range(size):
        if(arr[x] == -1):
            return false

        for y in range(size):
            if(mat[x][y] == 1 and arr[y] != -1):
                if(arr[x] == arr[y]):
                    return false
    return true

#Function to pick an assigned variable(state) for which any color is not assigned.
def getvar(mat):
    for i in range(0,9):
        for j in range(0,9):
            if mat[i][j] == 0:
                return i, j
    return -1, -1

#Function checks for solution, if not assigns a value for a variable and call the
# function recursively, if solution is found return true.
# Otherwise backtrack on the value which was assigned.
def doCSP(s):
    #1. check for solution if ok return true
    #2. get unassigned var
    #3. assign a value for var from domain in a loop and update assign
    #4. recursively call doCSP
    #5. check for return val, if true return true
    #6. backtrack the assignment

    #print(size, domain)
    #return
    #1

    #ans = s.validateBoard(solutionFound=True)
    ans = s.checkBoard()
    if (ans == 1):
        return 1
    if (ans == 2):
        return 2

    i, j = getvar(s.grid)
    if(i == -1 and j == -1):
        return 2

    #print(var)
    #check for each value of domain
    for c in range(1, 10):
        global search
        search = search + 1
        s.grid[i, j] = c

        #recursively to call doCSP
        ans = doCSP(s)
        if(ans == 2):
            return 2

        #backtrack due to failure
        s.grid[i, j] = 0

    return 1


#Function is part of AC3 algorithm. Which removes inconsistent values for
# basically arc between vhead and vtail variables and reduces the domains of
# vtail variable and updates the dommat 2D arrary. If any updates are done to
# dommat then it returns True otherwise it returns false.
#return true - if removed any domain values.
#return false - otherwise
def remove_inconsistent_values(vhead, vtail, mat, dommat, assign):
    ret = false
    flag = 0

    #if color is already assigned check for only neighbours and prune
    if(assign[vhead] != -1):    #it is already assigned a color
        setcolor = assign[vhead]
        for x in range(size):
            if(mat[vhead][x] == 1 and dommat[x][setcolor] == 1):
                flag = 1
                global prune
                prune = prune + 1
                dommat[x][setcolor] = 0
                ret = true
    else:
        #Check for all the arc from vtail->x and purne the value accordingly which are conflicting
        for x in range(domain):
            if(dommat[vtail][x] == 1):
                for y in range(domain):
                    if(x != y and dommat[vhead][y] == 1):
                        flag = 1
                        #break
                if(flag == 0):
                    #global prune
                    prune = prune + 1
                    dommat[vtail][x] = 0
                    ret = true

    return ret

#Function implements the AC3 – Arc Consistency algorithm.
# Iterates through all the arc’s and checks for any consistency issues and
# appropriately reduces the dommat with corresponding domain value.
def doac3_old(s, assign, dommat, var):
    #ans = []

    fifo = collections.deque()

    for x in range(size):
        if(mat[var][x] == 1 and assign[x] == -1):
            temp = [var, x]
            fifo.append(temp)

    #temp = [var, color]
    #fifo = collections.deque()
    #fifo.append(temp)

    while len(fifo) != 0:
        #if(var == 355):
        #    print (len(fifo))
        vhead, vtail = fifo.popleft()
        #print(var, col)

        #remove domain values from vtail
        res = remove_inconsistent_values(vhead, vtail, mat, dommat, assign)
        if(res == true):    #go through the neighbours of vtail and add them to queue
            for x in range(size):
                if(mat[vtail][x] == 1 and assign[x] == -1 and vhead != x):
                    #ans.append([x, col])
                    fifo.append([vtail,x])

        # check for any empty dommat -- This check may cause problems
        emp = 0
        for x in range(domain):
            if(dommat[vtail][x] == 1):
                emp = 1
        if emp == 0 :       ## no values in the domain are possible
            return false

    ##print(dommat)
    return true

def doac3(s, assign, dommat, var):
    global prune
    row = int(var / 9)
    col = var % 9
    k = box(var)

    boxarray = []
    t = np.transpose(s.grid)
    for i in range(BoxStartEndRange[str(k)][0][0], BoxStartEndRange[str(k)][0][1]):
        for j in range(BoxStartEndRange[str(k)][1][0], BoxStartEndRange[str(k)][1][1]):
            boxarray.append(i * 9 + j)

    v = assign[var]
    for x in range(0, 9):
        if(var != (row * 9 + x)):
            dommat[row * 9 + x][v - 1] = 0
            prune = prune + 1
        if(var !=  (x * 9 + col)):
            dommat[x * 9 + col][v - 1] = 0
            prune = prune + 1
        if(var != boxarray[x]):
            dommat[boxarray[x]][v - 1] = 0
            prune = prune + 1

    return true
#Function to revert the value removed
#not used now
def revertbackac3(mat, assign, dommat, ac3output):
    for var, col in ac3output:
        #print(var, col)
        dommat[var][col] = 1
    return

#Function implements the MCV – minimum constraint variable algorithm,
# where it reorder the variables based on the which variable is having
# the highest constraints compared to their neighbours.
def getvarplus(assign, dommat):
    domcnt = [0 for x in range(size)]
    m = 0x7ffffff
    ind = -1

    #go through for each neighbour who is not yet assigned
    for i in range(size):
        if (assign[i] == -1):
            #get the row count of 1's
            cnt = 0
            for j in range(domain):
                if(dommat[i][j] == 1):
                    cnt = cnt + 1
            domcnt[i] = cnt

            if(cnt < m):
                m = cnt
                ind = i
    return ind

boxmat = [0, 0, 0, 1, 1, 1, 2, 2, 2,
          0, 0, 0, 1, 1, 1, 2, 2, 2,
          0, 0, 0, 1, 1, 1, 2, 2, 2,
          3, 3, 3, 4, 4, 4, 5, 5, 5,
          3, 3, 3, 4, 4, 4, 5, 5, 5,
          3, 3, 3, 4, 4, 4, 5, 5, 5,
          6, 6, 6, 7, 7, 7, 8, 8, 8,
          6, 6, 6, 7, 7, 7, 8, 8, 8,
          6, 6, 6, 7, 7, 7, 8, 8, 8]
def box(var):
    return boxmat[var]


BoxStartEndRange = {
    '0': [(0, 3), (0, 3)], '1': [(0, 3), (3, 6)], '2': [(0, 3), (6, 9)],
    '3': [(3, 6), (0, 3)], '4': [(3, 6), (3, 6)], '5': [(3, 6), (6, 9)],
    '6': [(6, 9), (0, 3)], '7': [(6, 9), (3, 6)], '8': [(6, 9), (6, 9)]
}
#Function implements the LCV – Least constraint variable algorithm to reorder
# the color variables to indicate which color variable to pick up.
def reordercolor(var, s, dommat, assign):
    de = []

    # Check the with neighbours and try to find least constraint variable.
    row = int(var / 9)
    col = var % 9
    k = box(var)
    rowarray = []
    for x in range(0,9):
        rowarray.append(s.grid[row][x])

    boxarray = []
    t = np.transpose(s.grid)
    for i in range(BoxStartEndRange[str(k)][0][0], BoxStartEndRange[str(k)][0][1]):
        for j in range(BoxStartEndRange[str(k)][1][0], BoxStartEndRange[str(k)][1][1]):
            boxarray.append(s.grid[i][j])

    for x in range(domain):     ## pick a color
        if dommat[var][x] == 1:
            cnt = 3
            y = x + 1
            if (y in rowarray):
                cnt = cnt - 1
            if (y in t[col]):
                cnt = cnt - 1
            if (y in boxarray):
                cnt = cnt - 1
            de.append([cnt, y])

    de.sort(key = lambda tup:tup[0], reverse = True)
    colnew = [x[1] for x in de]

    return colnew

def checkconsistency(c, s, assign, var):
    # Check if the current color can be assigned if there is no clash
    row = int(var / 9)
    col = var % 9
    k = box(var)
    rowarray = []
    for x in range(0, 9):
        rowarray.append(s.grid[row][x])

    boxarray = []
    t = np.transpose(s.grid)
    for i in range(BoxStartEndRange[str(k)][0][0], BoxStartEndRange[str(k)][0][1]):
        for j in range(BoxStartEndRange[str(k)][1][0], BoxStartEndRange[str(k)][1][1]):
            boxarray.append(s.grid[i][j])

    if (c not in rowarray) and (c not in t[col]) and  (c not in boxarray):
        return true

    return false

#Function checks for solution, if not assigns a value for a variable and
# call the function recursively, if solution is found return true.
# Otherwise backtrack on the value which was assigned.
def do_dfs_plus(s, assign, dommat):
    # 1. check for solution if ok return true
    #ans = checksol(mat, assign)
    #if (ans == true):
    #    return true
    ans = s.checkBoard()
    if (ans == 1):
        return 1
    if (ans == 2):
        return 2

    # 2. get unassigned var
    var = getvarplus(assign, dommat)    # check for most constraint variable
    #var = getvar(assign)
    if (var == -1):
        return 2

    #print(var, assign[var])
    # 3. assign a value for var from domain in a loop and update assign
    colord = reordercolor(var, s, dommat, assign)
    #print (colord)
    #for c in range(domain):
    for c in colord:
        #check for consistency
        #if(dommat[var][c] == 1):
        if(checkconsistency(c, s, assign, var) == true):
            global search
            search = search + 1
            #assign the color A
            if assign[var] != -1:
                print("error this should never happen")

            assign[var] = c
            s.grid[int(var / 9)][var % 9] = c
            #print("assign[%d] = %d" % (var, c))
            #take backup of the allowed color and keep only A

            dommatbackup = [row[:] for row in dommat]

            for x in range(domain):
                dommat[var][x] = 0      # set all color to zero
                if(x == c):
                    dommat[var][x] = 1  # set selected color only - A

            result = doac3(s, assign, dommat, var)

            #TODO
            #check for any empty dommat -- This check may cause problems - TODO
            #if(result == true):
            #    return false

            #result = true
            if(result == true):
                # 4. recursively call doCSP
                ans = do_dfs_plus(s, assign, dommat)

                # 5. check for return val, if true return true
                if(ans == 2):
                    return 2

            # 6. backtrack the assignment
            assign[var] = -1
            s.grid[int(var / 9)][var % 9] = 0
            #revertbackac3(mat, assign, dommat, ac3output)
            #dommat[var] = dommatbackup[:]
            dommat = [row[:] for row in dommatbackup]

    return 1

#Just a driver function to run the do_dfs_plus function.
def dfs_CSP_plus(s):
    dommat = [[1 for x in range(domain)] for y in range(size)]
    #print (dommat)
    assign = [-1 for x in range(size)]

    for i in range(0, 9):
        for j in range(0, 9):
            if s.grid[i][j] != 0:
                dommat[i*9+j] = [0 for x in range(domain)]
                dommat[i*9+j][s.grid[i][j]-1] = 1
                assign[i*9+j] = s.grid[i][j]

    ans = do_dfs_plus(s, assign, dommat)

    return ans


if __name__ == '__main__':
#def main():
    ans = ""

    s = SudokuGenerator(".......12........3..23..4....18....5.6..7.8.......9.....85.....9...4.5..47...6...")
    #plus Time = 450575.784 millisecond,Number of search = 1114771
    #plusac3 - Time = 358912.367 millisecond, Number of search = 1229729
    #plus sc3 - Time = 281353.698 millisecond, Number of search = 1229729, Number of prune = 29513496
    #10
    #s = SudokuGenerator("78923164..56897312.2356497.2.4.7518.89.34275656791842.345786291912453867678129.34")
    #plus ac3 - Time = 3.438 millisecond, Number of search = 11, Number of prune = 264
    #20
    #s = SudokuGenerator(".4.798213.124.587997.132.4..8.24...775681932..23..69815.46871922.1.54768.67921435")
    #Time = 42463.812 millisecond, Number of search = 850534
    #plus Time = 7.159 millisecond, Number of search = 20
    #plus ac3 Time = 4.780 millisecond, Number of search = 21, Number of prune = 504
    #30
    #s = SudokuGenerator("879.3254621.4.587.5.67..2.3.57..932498..4.65.3.45...8.76892.4.51.235..6.4.5.871..")
    #plus Time = 9.664 millisecond , Number of search = 30
    #plus ac3 Time = 7.951 millisecond, Number of search = 32, Number of prune = 768
    s.generateBoard()

    domain = 9
    size = 81

    start = time.time()
    mode = 1
    if(mode == 0):
        ans = doCSP(s)
    else:
        ans = dfs_CSP_plus(s)
    end = (time.time() - start) * 1000

    #output the result
    if(ans == 2):
        print("Solution found ")
        print(s.grid)
    else:
        print("No answer")

    print("Time = %0.3f millisecond" % end)
    print("Number of search = %d" % search)
    if(mode == 1):
        print("Number of prune = %d" % prune)



