# a0

## route_pichu.py

### Search abstraction:
- Set of states: All houses that are available (not X houses) that pichu can be in.
- Initial state: The position of pichu at first 
- Goal state: pichu be in the same house that "@" is.
- Succesor function: L, R, U, D (4 houses that the pichu can go from the current house but if visited the move once it does not go that way) 
- Cost function: How many moves were performed

### Issues of the first version of the code:
It implments DFS as an algorithm to search. We know that if we have a loop in our graph, DFS can stuck in the loop. In this problem, since the pichu can get back to the previous house that it was in, the algorithm stuck in the loop (DFS is not complete). Also, it does not necessarly find the shortest path (DFS is not optimal).

### How to solve the issues:
I add another list to the fringe that keep the visited nodes in the path till the current position. By this, I avoid the loops so this problem solved.
In order to find the shortest path, I change the stack to priority queue (heuristic search). Each time, it checks the (move that has the shortest path from the first position) + (manhatan distance of the current house and the goal ) for the curent hous. In this way, it finds the shortest path.

### Suggestions:
There are some other ways that we can solve this problem. We could implement the BFS since it is both complete and optimal. But because the skeleton of the code was DFS, I tried to solve it using that.
Also we can solve it by some other heuristic functions. The heuristic function could be euclidian distance too. The g(x) will be the number of moves we take from the first position to current position 

## arrange_pichus.py

### Search abstraction:
- Set of states: Configuration of 0-k pichus in "." houses
- Initial state: The position of one fixed pichu at first 
- Goal state: Non-conflicting placement of k pichus
- Succesor function: Add queen to an empty square "." (each time that I add a pichu I make conflicting house with that pichu not available by using replacing "N" instead of "." )
- Cost function: Irrelevent

### Issues of the first version of the code:
The first version of the code used DFS shich is a good idea for this problem because we do not have any loops therefore it is complete for this problem. but it does not check the conflictings so it return results without considering it.

### How to solve the issues:
Each time that I add a pichu to the map, I replce conflicting house "." with new added pichu by "N" wich means that this house is not available for the other pichus.

### Suggestions:
I tried to solve it with a heuristic function but unfortunatley I could not find any good heuristic function.
based on the following link simple DFS and DFS with heuristics function does not have any difference in performance.

https://www.cs.unm.edu/~sdealy/nqueens_presentation.pdf 

