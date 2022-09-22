# a1-forrelease

## Part 1 - MAHSA

### a description of how you formulated the search problem,  including precisely defining the state space, the successor function, the edge weights, the goal state, and (if applicable)the heuristic function(s) you designed, including an argument for why they are admissible; 
I use A* search for this problem. I use the search algorithm 3 and try to find a consistent heuristic function.
 * state space: all configuration of 25 tiles.
 * successor func: we have moves (R1,L1,...). all the states after we apllied one of this moves on current state are our succors which is 24 states.
 * edge weights: it is 1 between each two nodes that are connected it means it take one moves to go to the next state from current state.
 * goal state: the state that all tiles are ordered from 1 to 25.
 * heuristic func:?

### a brief description of how your search algorithm works;
I use the A* without repeated states. (Search alg #3). It needs a consistent heuristic. it discarded the revisited states.
I have a fringe which has a priority queue structure. first I put my initial state in the fringe. each state is a tupple of (previous moves, heuristic cost, curr_state) (previous moves is a list of moves we take to get to the current state, heuristic cost is summation of number of moves it takes to get to this state and heuristic estimation of number of moves we need to get to the goal state, and curr_state is the board we are in it now).
I pop the state from the fringe that has the minimum heuristic cost each time.(which means it is more promissing). I add it to the closed list which means I see it once. I checked wether the state that I take from my fringe is a goal state or not. if it is a goal state so I just return the previous moves it takes to get to this state. else I look into the successors of this state. if the successor is in the closed list means I visit it once so i just discard it. else I look if I have this succesor in my fringe. if there was same successor in my fringe which took more steps to get there I remove it and add the new one to the successor. At the end I check if my successor is not in the fringe I add it to the finge.  
### discussion of any problems you faced, any assumptions,simplifications, and/or design decisions you made.
Finding a heuristic function which is consistent was very hard. I explain all of the heuristics that I used and didn't work (All works for the board0.txt):

1. I used the manhattan distance but not the uisual one. for each tile I checked wether it is nearer to go left or right, up or down. I commnet my heuristic funtion and I write #heuristic #1 above it. Then we know that each time the manhattan distance can change at most by 16. so I add all the manhattan distance and devide it by 16.
    TA told me maybe it's not consistent but neither of us(TA and I ) could not find a counterexample.

```python

def heuristic_func(state):
    man_dist = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            val_row = (state[row][col]-1)//5
            val_col = (state[row][col]-1)%5
            man_dist +=min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
    return (man_dist/16)
```
2. I used number of mispaced tiles devided by 16 (again I devided by 16 becasue each time the number of misplaced tiles can be change by at most 16). it didn't work too but it is consistent too. I comment it as a heuistic #2

```python
def heuristic_func(state):
    mismathced_tiles = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            if (((state[row][col]-1)//5 != row) or ((state[row][col]-1)%5 != col)):
                mismathced_tiles+=1
    return mismathced_tiles/16
```

3. I combined #1 and #2 and get average but again didn't get anything.

```python
def heuristic_func(state):
    man_dist = 0
    ans = 0
    mismathced_tiles = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            val_row = (state[row][col]-1)//5
            val_col = (state[row][col]-1)%5
            if ((val_row!= row) or (val_col != col)):
                mismathced_tiles+=1
            
            man_dist =min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
            if man_dist>ans:
                ans = man_dist
    if mismathced_tiles>=1:
        return (ans+((mismathced_tiles-1)/15))/2
    else:
        return 0
```

4. In this one I add all the misplaced tiles in the outer part devided by 16, add the all the misplaced tiles in the inner part and devided by 8 and at last I add the previous oned with the center tile if it is misplaced.

```python
def heuristic_func(state):
    mismathced_tiles = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            val_row = (state[row][col]-1)//5
            val_col = (state[row][col]-1)%5

            if ((val_row!= row) or (val_col != col)):
                if (row == 0 or row == 4 or col == 0 or col == 4): 
                    mismathced_tiles+=1/16
                elif (row == 1 or row == 3 or col == 3 or col == 3):
                    mismathced_tiles+=1/8
                else:
                    mismathced_tiles+=1/5
    return mismathced_tiles
```

5. In this one I use the manhattan distance(not the usual one the one that explain in #1) I calculate it for each tile and get the maximum as a heuristic cost.

```python
def heuristic_func(state):
    man_dist = 0
    ans = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            val_row = (state[row][col]-1)//5
            val_col = (state[row][col]-1)%5
            man_dist =min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
            if man_dist>ans:
                ans = man_dist
    return ans
```

6. I uesd the Idea of #1 and #4 together

```python
def heuristic_func(state):
    man_dist = 0
    ans = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            val_row = (state[row][col]-1)//5
            val_col = (state[row][col]-1)%5
            if (row == 0 or row == 4 or col == 0 or col == 4):
                man_dist +=(min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col)))/16
                man_dist = man_dist/16
            elif(row == 1 or row == 3 or col == 1 or col == 3):
                man_dist +=(min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col)))/8
            else:
                man_dist +=(min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col)))/5
    return man_dist
```

7. I used the # of misplaced tiles which is not admissible but the funny part is that it works for both board0.txt and board0.5.txt LOL.

```python
def heuristic_func(state):
    mismathced_tiles = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            if (((state[row][col]-1)//5 != row) or ((state[row][col]-1)%5 != col)):
                mismathced_tiles+=1
    return mismathced_tiles
```

8. get maximum of heuristic #4 and heuristic #5

```python
def heuristic_func(state):
    man_dist = 0
    ans = 0
    mismathced_tiles = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            
            val_row = (state[row][col]-1)//5
            val_col = (state[row][col]-1)%5

            man_dist =min(abs(row-val_row),5-abs(row-val_row))+min(abs(col-val_col), 5-abs(col-val_col))
            if man_dist>ans:
                ans = man_dist

            if ((val_row!= row) or (val_col != col)):
                if (row == 0 or row == 4 or col == 0 or col == 4): 
                    mismathced_tiles+=1/16
                elif (row == 1 or row == 3 or col == 3 or col == 3):
                    mismathced_tiles+=1/8
                else:
                    mismathced_tiles+=1/5
    return max(mismathced_tiles, ans)
```
9. calculate mismatched rows (out of row) and mismatched column (out of column) for each tile. and devide the sum by 8 because at most number of mismatched rows or columns can change by 8.

```python
def heuristic_func(state):
    mismathced_rows = 0
    mismatched_cols = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            if (((state[row][col]-1)//5) != row):
                mismathced_rows+=1
            if(((state[row][col]-1)%5) != col):
                mismatched_cols+=1
    return (mismathced_rows+mismatched_cols)/8
```


## Part 2 - ZACH
The state space consists of all cities within the road-segments file, where the connections between these cities are highways, also contained within the road-segments file. The start state and goal state are passed to the get_route() function as “start” and “end”. The next state is decided using the A-star search algorithm, so nodes on the fringe are expanded if they have the minimum value of f(n) = g(n) + h(n), where g(n) is the cost to get to the present node, and h(n) is the cost to move to the corresponding node in the fringe. Because we know the cost to get to every node in the state space, we do not need a heuristic function, and instead just use the cost function (because we’re using the actual cost, the cost is never overestimated, thus, is admissible). The cost was specified by the argument “cost”, and could be one of “segments”, “distance”, “time”, or “delivery”. The segments cost function just took into account the number of nodes visited, distance took into account the distance from one node to the next, time took into account the time to get from one node to the next, and delivery took into account the estimated time it would take to make a delivery from one node to the next. 

The main challenge was keeping track of all of the cost values and the route taken, so they could be returned when the goal node is found. To do this, I used dictionaries for each of the cost functions, where the key is a city, and the value is the city's current f value, and a dictionary that contained each city explored, and it’s parent node, so the route could be retraced. No matter which cost function was used, I updated the dictionaries exactly the same, and the only difference was in the process of selecting the node to be explored. A necessary assumption I made, that presented challenges early in the coding process, is that you could travel back and forth between cities using the corresponding highway. In the beginning of the coding process, I assumed the first city listed was the origin, and the second city listed was the destination. However, I was not able to find a path in the test case with this assumption. Thus, I had to write a function called get_destination(line, origin), where the line is the appropriate line from the road-segments file, and the origin is the city we’re traveling from. This helped me find the next nodes to be added to the fringe.


## Part 3 - CODE: ZACH | WRITING: MAHSA


###  a description of how you formulated the search problem,  including precisely defining the state space, the successor function, the edge weights, the goal state
 We know that local search is used for pathless problems. This problem is a pathless problem therefore we used local search. In local search, it just remember the current state, there is no need for fringe, so we require much less memory. In this problem we want to find the state that has a minimum cost (cost means that total amount of time the staff needs to do works, subject to the constraint that no team may have more than 3 students.)

* state space: all configurtions of the teams we could have
* successor func: using combine or seoerate in mutate function to change the looser state to new state. that new state is a successor
* goal state: the state with minimum cost (cost means that total amount of time the staff needs to do works, subject to the constraint that no team may have more than 3 students.)

### a brief description of how your search algorithm works; 
We used genetic algorithm for this problem. 

step1: First we generate 1000 random states (each state is a configuration of teams we could have). Then we find the most promissing one among these 1000 states (the one that has the lowest cost). 

step2: Then we choose 2 states randomly from those 1000 states. compare their cost and choose the one that has more cost set it as a looser.
then we are looking at teams in our looser state, by probabilty of 0.5 we split teams and by probability of 0.5 we combine some teams. 
For split part, we choose one of the teams that has more than one member randomly and again split it randomly into new teams.
For combine part, we choose 2 teams that has less than 3 members randomly and combine them and make new team/teams. 

Then we replace this new state with the looser state and add it to our list of states if it's not in it already

we do the step 2 for 500 times

step3: Now in our new list of states we check that whether there is any promissing state that has less cost than previous best state we found and if it is we replace the new one as a goal.

We do step 2 and 3 in the while loop and each time we get the better solution till the time constraint end or we reach a state that contains 3 member teams only and there is no other complains about the teams.

### discussion of any problems you faced, any assumptions,simplifications, and/or design decisions you made

One difficulty I had was decided which states to explore, because there seemed to be no systematic way to expand fringe nodes. This is why I decided to use a GA for this problem. I created a function to randomly produce lists of teams, and another function to randomly mutate an existing list of teams. This way, I did not have to choose how to expand the fringe, and by using a GA style of optimization, I was not just randomly searching the search space. 

I simplified the standard GA approach. Instead of using 0's and 1's for the population and some function to transform a list of 0's and 1's into a list of teams, I simply just used the lists of teams. Moreover, the winner is not used to mutate the loser, which is common in GA's. The reason I decided against this is because, due to the nature of the problem, I felt that it would not benefit the search. For a list of teams to have a low cost, all teams would have to be matched well. Thus, taking half the teams and switching the rest did not feel like it would be beneficial enough to try to implement.
