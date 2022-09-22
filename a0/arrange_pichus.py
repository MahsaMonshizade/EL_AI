#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Mahsa Monshizadeh (mmonshiz)]
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Return the location of first pichu on the map
def find_first_pichu(house_map):
    for row in range(len(house_map)):
        for col in range(len(house_map[0])):
            if house_map[row][col] == "p":
                return row, col

# It puts N (not available) in the houses that has the same row as the added pichu (according to x's) and return the new map 
def check_row(original_house_map, row, col):
    house_map = []
    for i in range(0, len(original_house_map)):
        tmp = []
        for j in range(0, len(original_house_map[0])):
            tmp.append(original_house_map[i][j])
        house_map.append(tmp)
    if col < len(house_map[0])-1:
        for c in range (col+1,len(house_map[0])):
            if (house_map[row][c] == "."):
                house_map[row][c] = "N"
            elif (house_map[row][c] == "X" or house_map[row][c] == "@"):
                break
    if col>0:
        for c in range(col-1, -1, -1):
            if (house_map[row][c] == "."):
                house_map[row][c] = "N"
            elif (house_map[row][c] == "X" or house_map[row][c] == "@"):
                break
    return house_map

# It puts N (not available) in the houses that has the same column as the added pichu (according to x's) and return the new map
def check_col(original_house_map, row, col):
    house_map = []
    for i in range(0, len(original_house_map)):
        tmp = []
        for j in range(0, len(original_house_map[0])):
            tmp.append(original_house_map[i][j])
        house_map.append(tmp)
    if row < len(house_map)-1:
        for r in range (row+1,len(house_map)):
            if (house_map[r][col] == "."):
                house_map[r][col] = "N"
            elif (house_map[r][col] == "X" or house_map[r][col] == "@"):
                break
    if row>0:
        for r in range(row-1, -1, -1):
            if (house_map[r][col] == "."):
                house_map[r][col] = "N"
            elif (house_map[r][col] == "X" or house_map[r][col] == "@"):
                break
    return house_map

# It puts N (not available) in the houses that has the same diagonals as the added pichu (according to x's) and return the new map
def check_diagonal(original_house_map, row, col):
    house_map = []
    for i in range(0, len(original_house_map)):
        tmp = []
        for j in range(0, len(original_house_map[0])):
            tmp.append(original_house_map[i][j])
        house_map.append(tmp)
    if(row<len(house_map)-1 and col<len(house_map[0])-1):
        r = row+1
        c = col+1
        while(r<len(house_map) and c<len(house_map[0])):
            if house_map[r][c] == ".":
                house_map[r][c] = "N"
            elif(house_map[r][c] == "X" or house_map[r][c] == "@"):
                break
            r+=1
            c+=1
    
    if(row>0 and col>0):
        r = row-1
        c = col-1
        while(r>-1 and c>-1):
            if house_map[r][c] == ".":
                house_map[r][c] = "N"
            elif(house_map[r][c] == "X" or house_map[r][c] == "@"):
                break
            r-=1
            c-=1

    if row>0 and col<len(house_map[0])-1:
        r = row-1
        c = col+1
        while r>-1 and c<len(house_map[0]):
            if house_map[r][c] == ".":
                house_map[r][c] = "N"
            elif house_map[r][c] == "X" or house_map[r][c] == "@":
                break  
            r-=1
            c+=1

    if row<len(house_map)-1 and col>0:
        r = row+1
        c = col-1
        while r<len(house_map) and c>-1:
            if house_map[r][c] == ".":
                house_map[r][c] = "N"
            elif house_map[r][c] == "X" or house_map[r][c] == "@":
                break  
            r+=1
            c-=1 
    return house_map       

# Replacing "N" with "." and return new map
def remove_Ns(house_map):
    for r in range(len(house_map)):
        for c in range(len(house_map[0])):
            if house_map[r][c] == "N":
                house_map[r][c] = "."
    return house_map

# Add a pichu to the house_map at the given position and put "N" in the houses that becaome unavailable for the other picus, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    house_map = check_row(house_map, row, col)
    house_map = check_col(house_map, row, col)
    house_map = check_diagonal(house_map, row, col)
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    first_p_row, first_p_col = find_first_pichu(initial_house_map)
    initial_house_map = check_row(initial_house_map, first_p_row, first_p_col)
    initial_house_map = check_col(initial_house_map, first_p_row, first_p_col)
    initial_house_map = check_diagonal(initial_house_map, first_p_row, first_p_col)
    fringe = [initial_house_map]
    round = 0
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                new_house_map = remove_Ns(new_house_map)
                return(new_house_map,True)
            fringe.append(new_house_map)
        round+=1
            

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    if solution == None:
        print("False")
    else:
        print (printable_house_map(solution[0]) if solution[1] else "False")


