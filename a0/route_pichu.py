#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Mahsa Monshizadeh (mmonshiz)]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

#return the position of the goal in the map
def goal_pos(map):
        for r in range(len(map)):
                for c in range(len(map[0])):
                        if map[r][c] == "@":
                                return (r, c)
#return manhattan distance between two house
def manhatan_distance(house1, house2):
        return abs(house1[0]-house2[0])+abs(house1[1]-house2[1])
# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        goal = goal_pos(house_map)

        # Fringe is a list of tuples that in each tuple store the curr_move, some of the distance from the first location and manhattan distance from goal, a list of the nodes it meets in the path and a distance from the first location
        fringe=[(pichu_loc,manhatan_distance(goal, pichu_loc),[], 0)]

        while fringe:
                # Inverse sort fringe based on the distance from the first location 
                fringe = sorted(fringe, key=lambda x:(-x[1],x[0]))
                (curr_move, heuristic, curr_path, curr_dist)=fringe.pop()
                
                for move in moves(house_map, *curr_move):
                        if house_map[move[0]][move[1]]=="@":
                                curr_path.append(move)
                                previous_loc = pichu_loc
                                path = ""
                                for loc in curr_path:
                                        if loc[0] ==  previous_loc[0]-1:
                                                path += "U"
                                        elif loc[0] ==  previous_loc[0]+1:
                                                path += "D"
                                        elif loc[1] ==  previous_loc[1]-1:
                                                path += "L"
                                        elif loc[1] ==  previous_loc[1]+1:
                                                path += "R"
                                        previous_loc = loc
                                return (curr_dist+1, path)  # return the shortest distance from first location and the path
                        else:
                                if move not in curr_path:
                                        new_curr_path = curr_path + [move]
                                        fringe.append((move, curr_dist+1+manhatan_distance(move, goal) , new_curr_path, curr_dist+1))

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

