# a0
#Edited by Aakash Sarnobat username: asarnoba
## <u>**Assignment 0: Searching and Python**</u>

 

<u>**Part 1: Navigation**</u>

 **Abstraction:-**

**Set of valid states**: Valid states are the empty squares where the agent p can fly over represented by a ''."

**Successor function**: Function which considers the agent’s current location and returns the possible positions for the agent's next move taking into account the different constraints like walls where the agent can't fly over.

**Cost function:** Cost function here would be uniform as each step incurs cost of 1.

**Initial State**: Agent p in the start location as given in the input map.

**Goal state:** Goal state is the state when the agent reaches the position '@'


The given program fails often because when the agent reaches the position (2,2) considering 0-based indexing it keeps on going to the same successor states  which lead to the wall and this goes on as we don't keep a track of positions or states already visited.

As a solution to this, the following changes were made to the search() function-When we traverse through the fringe we try to implement BFS here and take a new variable 'steps' which will help us know the depth of the search. We also take the 'size' variable which is the length of the fringe. Also we pop the first element of the list fringe instead of pop() which was earlier returning the last element of the list. To keep a track of the nodes already visited we are marking them with the alphabet 'T'. Also for tracing the path we add one parameter to the moves list for the direction which we denote as R for right L for Left U for Up and D for Down. Every time we append to the fringe list we add the new parameter direction which is 'dir + dir_new' which is previous direction string till now and the new direction.

**Challenges faced:**

Tracing the path was difficult which made me mark all the visited positions with a letter T so that they are not revisited and also for the directions I had to change the function definition adding one more parameter for the direction code.

<u>**Part 2:  Hide-and-seek**</u>

**Abstraction:-**

**Set of valid states:** Valid states are the one where the positions of agent P are such that no other agent can see each other directly.

**Successor function:** Function which returns a position for the placement of next agent P such that it is not seen by any other agent.

**Cost function:** Cost function here would be uniform as each step incurs cost of 1.

**Initial State**: Agent p in the start location as given in the input map.

**Goal state:**  Goal state is the state when all the agents p are placed on the board such that none of them are visible to each other.

**Implementation approach:**

Firstly we update the successor() function and add a check for rows and columns which will help check the valid placements in any given row and column. In these functions we are checking if there exists an agent 'p' in the neighboring columns, if yes then we return false as we don't want to place it in that position. Alternatively if we find a 'X' or a '@' we return a flag true which indicates it is safe for placement of the agent.

After the successor function returns the valid states we keep a list of visited nodes in the solve() function which helps us to avoid nodes being revisited.

**Challenges faced:**

Checking conditions for valid column and rows and also to identify the diagonal positions which is not yet implemented in the code. To identify if two agents are on the same diagonal I figured out that the absolute difference between their rows and columns should be the same.
