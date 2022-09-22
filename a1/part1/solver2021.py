#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Mahsa Monshizadeh 2000757990
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import copy
from operator import itemgetter, attrgetter, le


ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    # succ = [(move, new_state)]
    succ = []

    # L moves
    for row in range(5):
        new_state = copy.deepcopy(state)
        tmp = new_state[row][0]
        for i in range(4):
            new_state[row][i] = new_state[row][i+1]
        new_state[row][4] = tmp
        succ.append(("L"+str(row+1), new_state))

    # R moves
    for row in range(5):
        new_state = copy.deepcopy(state)
        tmp = new_state[row][4]
        for i in range(4, 0, -1):
            new_state[row][i] = new_state[row][i-1]
        new_state[row][0] = tmp
        succ.append(("R"+str(row+1), new_state))
    
    # U moves
    for col in range(5):
        new_state = copy.deepcopy(state)
        tmp = new_state[0][col]
        for i in range(4):
            new_state[i][col] = new_state[i+1][col]
        new_state[4][col] = tmp
        succ.append(("U"+str(col+1), new_state))

    # D moves
    for col in range(5):
        new_state = copy.deepcopy(state)
        tmp = new_state[4][col]
        for i in range(4, 0, -1):
            new_state[i][col] = new_state[i-1][col]
        new_state[0][col] = tmp
        succ.append(("D"+str(col+1), new_state))
    
    # Oc
    new_state = copy.deepcopy(state)
    tmp = new_state[0][0]
    for r in range(4):
        new_state[r][0] = new_state[r+1][0]
    for c in range(4):
        new_state[4][c] = new_state[4][c+1]
    for r in range(4, 0, -1):
        new_state[r][4] = new_state[r-1][4]
    for c in range(4, 1, -1):
        new_state[0][c] = new_state[0][c-1]
    new_state[0][1] = tmp
    succ.append(("Oc", new_state))

    # Occ
    new_state = copy.deepcopy(state)
    tmp = new_state[0][4]
    for r in range(4):
        new_state[r][4] = new_state[r+1][4]
    for c in range(4, 0, -1):
        new_state[4][c] = new_state[4][c-1]
    for r in range(4, 0, -1):
        new_state[r][0] = new_state[r-1][0]
    for c in range(3):
        new_state[0][c] = new_state[0][c+1]
    new_state[0][3] = tmp
    succ.append(("Occ", new_state))

    # Ic
    new_state = copy.deepcopy(state)
    tmp = new_state[1][1]
    new_state[1][1] = new_state[2][1]
    new_state[2][1] = new_state[3][1]
    new_state[3][1] = new_state[3][2]
    new_state[3][2] = new_state[3][3]
    new_state[3][3] = new_state[2][3]
    new_state[2][3] = new_state[1][3]
    new_state[1][3] = new_state[1][2]
    new_state[1][2] = tmp
    succ.append(("Ic", new_state))

    #Icc
    new_state = copy.deepcopy(state)
    tmp = new_state[1][3]
    new_state[1][3] = new_state[2][3]
    new_state[2][3] = new_state[3][3]
    new_state[3][3] = new_state[3][2]
    new_state[3][2] = new_state[3][1]
    new_state[3][1] = new_state[2][1]
    new_state[2][1] = new_state[1][1]
    new_state[1][1] = new_state[1][2]
    new_state[1][2] = tmp
    succ.append(("Icc", new_state))

    return succ

# check if we've reached the goal
def is_goal(state):
    goal_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    if state == goal_state:
        return True
    return False


#heuristic #1

# def heuristic_func(state):
#     man_dist = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             val_row = (state[row][col]-1)//5
#             val_col = (state[row][col]-1)%5
#             man_dist +=min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
#     return (man_dist/16)


# heuristic #2

# def heuristic_func(state):
#     mismathced_tiles = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             if (((state[row][col]-1)//5 != row) or ((state[row][col]-1)%5 != col)):
#                 mismathced_tiles+=1
#     return mismathced_tiles/16


# heuristic #3

# def heuristic_func(state):
#     man_dist = 0
#     ans = 0
#     mismathced_tiles = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             val_row = (state[row][col]-1)//5
#             val_col = (state[row][col]-1)%5
#             if ((val_row!= row) or (val_col != col)):
#                 mismathced_tiles+=1
            
#             man_dist =min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
#             if man_dist>ans:
#                 ans = man_dist
#     if mismathced_tiles>=1:
#         return (ans+((mismathced_tiles-1)/15))/2
#     else:
#         return 0



#heuristic #4

# def heuristic_func(state):
#     mismathced_tiles = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             val_row = (state[row][col]-1)//5
#             val_col = (state[row][col]-1)%5

#             if ((val_row!= row) or (val_col != col)):
#                 if (row == 0 or row == 4 or col == 0 or col == 4): 
#                     mismathced_tiles+=1/16
#                 elif (row == 1 or row == 3 or col == 3 or col == 3):
#                     mismathced_tiles+=1/8
#                 else:
#                     mismathced_tiles+=1/5
#     return mismathced_tiles


# heuristic #5

# def heuristic_func(state):
#     man_dist = 0
#     ans = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             val_row = (state[row][col]-1)//5
#             val_col = (state[row][col]-1)%5
#             man_dist =min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
#             if man_dist>ans:
#                 ans = man_dist
#     return ans


# heuristic #6

# def heuristic_func(state):
#     man_dist = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             val_row = (state[row][col]-1)//5
#             val_col = (state[row][col]-1)%5
#             if (row == 0 or row == 4 or col == 0 or col == 4):
#                 man_dist +=((min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col)))/16)
#             elif(row == 1 or row == 3 or col == 1 or col == 3):
#                 man_dist +=((min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col)))/8)
#             else:
#                 man_dist +=((min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col)))/5)
#     return man_dist


# heuristic 7

def heuristic_func(state):
    mismathced_tiles = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            if (((state[row][col]-1)//5 != row) or ((state[row][col]-1)%5 != col)):
                mismathced_tiles+=1
    return mismathced_tiles


# heuristic 8

# def heuristic_func(state):
#     man_dist = 0
#     ans = 0
#     mismathced_tiles = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
            
#             val_row = (state[row][col]-1)//5
#             val_col = (state[row][col]-1)%5

#             man_dist =min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
#             if man_dist>ans:
#                 ans = man_dist

#             if ((val_row!= row) or (val_col != col)):
#                 if (row == 0 or row == 4 or col == 0 or col == 4): 
#                     mismathced_tiles+=1/16
#                 elif (row == 1 or row == 3 or col == 3 or col == 3):
#                     mismathced_tiles+=1/8
#                 else:
#                     mismathced_tiles+=1/5
#     return max(mismathced_tiles, ans)


# heuristic 9

# def heuristic_func(state):
#     mismathced_rows = 0
#     mismatched_cols = 0
#     for row in range(len(state)):
#         for col in range(len(state[0])):
#             if (((state[row][col]-1)//5) != row):
#                 mismathced_rows+=1
#             if(((state[row][col]-1)%5) != col):
#                 mismatched_cols+=1
#     return (mismathced_rows+mismatched_cols)/8


def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # convert tupple initial board to list initial board
    initial_board = list(initial_board)
    initial_state = []
    for i in range(5):
        initial_state.append(initial_board[5*i: 5*i+5])
    heuristic_cost = heuristic_func(initial_state) 
    # fringe is list of tupples. each tupples contains (previous moves,heuristic_func, current_state) 
    fringe = [([], heuristic_cost, initial_state)]
    closed = []
    
    while fringe:
        # Inverse sort fringe based on the heuristic cost
        fringe = sorted(fringe, key= itemgetter(1), reverse=True )
        (previous_moves, heuristic_cost, curr_state)=fringe.pop()
        print(len(fringe))
        print(previous_moves)
        print(heuristic_cost)
        print("\n")
        closed.append(curr_state)
        if is_goal(curr_state):
            return previous_moves  
        for move in successors(curr_state):
            if move[1] in closed:
                continue
            new_previous_moves = previous_moves+[move[0]]
            new_heuristic_cost = heuristic_func(move[1]) + len(new_previous_moves)
            flag = True
            br_flag = False
            for tupp in fringe:
                if(tupp[2] == move[1]):
                    flag = False
                    if (len(tupp[0])>len(new_previous_moves)):
                        fringe.remove(tupp)
                        fringe.append((new_previous_moves, new_heuristic_cost, move[1]))
                        br_flag = True
                        break
                if br_flag:
                    break
            
            if flag:
                fringe.append((new_previous_moves, new_heuristic_cost, move[1]))


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))


    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
