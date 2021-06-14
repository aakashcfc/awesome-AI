# a1
**Assignment 1**

**Part 1: The 2021 Puzzle**

Q1. What is the initial state?

A: The initial state is the input configuration which we are reading from the files.

Q2. What is the successor function?

A: The successor function are all the combination of the board where it can slide 1st and 3rd rows to the left and 2nd and 4th rows to the right, wrapping around to the other side of the board. And for the columns, 1st, 3rd and 5th column to up and 2nd and 4th column down in wrapping around way. So each state can generate 9 successor combinations

Q3. What is the cost function?

A: When we slide a row or column our cost increase by 1.

Q4 What is the Heuristic function?

A: Number of misplaced titles from the goal states divided by 5 is the heuristic function we are using. We are dividing it by 5 so that it don&#39;t overestimates from h\*(s). We took 5 based on the logic of Max(No. of row, column)

Q5. What is the goal state definition?

| 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- |
| 6 | 7 | 8 | 9 | 10 |
| 11 | 12 | 13 | 14 | 15 |
| 16 | 17 | 18 | 19 | 20 |

A:

Approach:

1. We defined our initial state, heuristic function, goal state, successor state based on the above logic
2. We converted our input file into Numpy matrix to do the matrix manipulation to generate our successor state
3. We implemented A\* search: Created heap fringe where it pops the state based on the lowest value of heuristic + cost function and return the slides it took to reach the goal state

Functions created:

1. Leftshift : Do the left slide wrapping around other side
2. Rightshift: Do the right slide wrapping around other side

1. numpy\_matrix: Converts the data into Numpy matrix
2. successors: Generates successor. Each states generate 9 successors
3. is\_goal: To check if it&#39;s a goal state
4. heurestic\_func: Heuristic function, based on number of misplaced slides/5
5. solve: A\* implementation

**Part 2: Road trip!**

Abstraction:
 Initial state: The starting city
 Goal state: A route path from the starting to the goal city.
 Cost function: Can be one from distance,time,segments,safe

Implementation:

Retrieve the road-segments and city-gps data from the files &#39;road-segments.txt&#39; and &#39;city-gps.txt&#39; files. We are using heapq to store our fringe. Calculate priority index based on the cost function to be used. We store our fringe in the following format:

(route\_so\_far, miles\_so\_far, segments\_so\_far, time\_elapsed\_so\_far, accidents\_so\_far)

Heuristics:

1. Distance:  To choose a path that has the shortest distance from start city to the goal city.

Choice of function: We choose Haversine distance to find out the circular distance between two of the start and end city. This choice helps us to find the circular distance between two coordinates.

1. Time: To choose a path that takes the shortest time to cover from the start city to the goal city

Choice of function: We calculate the time taken by considering the haversine distance between the cities divided by the maximum speed considered which will give us the actual time taken to reach the destination. This way we can ensure that the cost function never overestimates the goal state.

1. Segments: Goal is to find least number of edges to be covered in the graph. Here we assume each edge as cost 1.
2. Safe: We have used two functions. 1 to calculate accidents in highways(=distance\_covered/1000000) and other to calculate accidents in other roads((=2\*distance\_covered/1000000)).

Challenges: Finding a good heuristic function to calculate the path with least number of accidents . This involved keeping a track of all the possible cities visited before and to consider the ones only with lesser count.

**Part 3: Choosing teams**

1.Initial State:

All the users are alloted alone for project groups.

2. Successor states:

The possible combination of team members from the current state which has less cost when compared to previous state.

3. Cost Function:

1. Requested team size is not allocated.

2. The preferred team members are not allocated to the user.

3. The not preferred team members are allocated to the user.

4. Goal State:

The successor state obtained from initial state which has optimal cost when compared to other states.

Implementation (A\* Search):

1. Firstly, the initial state is stored in a fringe with the cost function and yielding the team and its cost.
2. The visited state is stored in a separate list to avoid redundancies.
3. The successor states are generated from the current states using combinations() from itertools from which valid states are taken and the successor states with the cost less than the previous state will be yielded.
4. The successor states with cost greater than the previous state will be skipped.

Difficulties Faced:

Firstly, we have tried to obtain the successor state using local search. When the user prefers to work alone, that user is saved to final list without pairing with others. And the remaining users are paired according to their preferences and non-preferences. When all the pairing is done based on their preferences, and if any user is left out without pairing those users will be paired with maximum of 2 members. But in this method, we are able to achieve only one successor state and hence we are to produce only one cost.

Secondly, We have saved the initial state and its cost to a priority queue and yielding the initial state and cost. Then the pair with highest cost is picked and paired with the other pairs if the total users is less than or equal to 3. Then among the pairs the pair with lowest cost taken and appended with rest pairs in the previous state. In this method, we are not able to obtain the optimal cost.