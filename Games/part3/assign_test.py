#(1) a description of how you formulated the search problem, including precisely dening the state space, the successor function,
#the edge weights, the goal state, and (if applicable) the heuristic function(s) you designed, including an
#argument for why they are admissible;

#Answer: So the problem statement for this quetsion is to to reduce the K,M,N time which is reduce the no of time to correct
#assignment which depends on the number of teams which is the K factor, Secondly reducing the N factor that is grouping them
#with the desired team number and member and thirdly M which is not grouping them with the non [refred member.
#Initial state: I assumed my initial state to be member with highest time
#Goal state: to reduce time of each highest member to the lowest by groupig it with other memebers in group of two/ three.
# If grouping reduces its individual cost, else leave it alone.
#sucessor function : individual with their costs, all possible combinations with rest of members in group of two or three and
# their time. #the edge weight: total time taken by considering factors like m, n and 1 min(meeting with instructor)  involved.

#(2) a brief description of how your search algorithm works;
# 1) Taking my input file and breaking each line and storing it in the list
#2) Secondly I am taking a dictionary for group size, prefer member and non prefermeber
#3)Now slpitting everuthing for example I am storing my user 1 along with theor prefred memebr in dictionar
#4) secondly i am splitting an storing the group prefrence of each user
#5) thirdly i am storing the non prefred memeber they have listed. In all, I am dividing each and every part of the file which
#was entered into different dictionary so that it can be accessable easily so now i have seperate information for all user
#user with prefer group number, user with prefer number, user with non prefer memeber
#6)Firstly my team is grouped single, I am conidering every member to be team alone and I am calculating the cost for each team
#i.e single team so now each user has a number associated with them which is the cost. I am using cost_function() to calculate
#the cost for the team.
#7 I am taking a priority queue to sort my list so the member with highest cost will come out first and then I can group that memebr
#with other member and check their cost if that cost is less than the initial cost or not
#8 so now my one meber comes out the priority queue, i will group that member with remianing other member and calculate that cost
#while looking at the other values provided such as prefred member, no prefer memebr and group size
#9 now after calculating the cost for all i will pick this group of 2(A,B suppose) who have the least cost and push them in the
#list of my team so now my team has suppose {AB, C, D, E, F}. Now each have their cost associated with it . Now I will again
#pick up the team with highest cost and try to minimize the cost using the same procedure suppose among all AB have the highest
# cost , Now I will again try to group that with other member so now {ABC,D,E,F} so now I will have the cost so once my team is
#made of three and the cost is less as compared to the previous cost , I will pust that out and proceed with other members and
#group them
#10 So at the end I will have my team grouped with other memeber, and with the cost which is less than the initial cost.
#11 In case 'test' size = 2 or 1(it will happen if number of member size is not divisible by 3), it groups them togther and
# calculates its time and prints them.

#(3) any discussion of any problems you faced, any assumptions, simplications, and/or design decisions you made.
#Answer: Firstly I tried the combination thing of generating all the possible states, such as groouping A with B, C,D,E,F
#and then taking the group with lowest number and trying to minimize again with grouping it with ABC,ABD,ABE, ABF , but in case
#of small data it works properly but with large number , the states generation was high and redundancy was there, so I modified
#algorithm as above to optimize and return the result in minimum time possible. The current solution is the optimal solution
# The logic is mine and I discussed with Umang mehta to clarify it and make it more optimal.


import os
import sys
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
k = 4
m = 5
n = 2

#input_file = sys.argv[1]
'''k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])'''

input_file = "D:/SEM-1/ElementsOfAI/asarnoba-deelango-sk128-a1-master/part3/test1.txt"
#reading from the file
file = open(input_file , 'r')
input_list = []
for line in file:
    input_list.append(line.split())
#print(input_list)


pref = {}
non_pref = {}
group_size = {}

for inputlist in range(0, len(input_list)):
    group_size[input_list[inputlist][0]] = int(input_list[inputlist][1])

for inputlist in range(0, len(input_list)):
    if input_list[inputlist][2] == '_':
        pref[input_list[inputlist][0]] = []

    else:

        pref_mem_list = input_list[inputlist][2].split(",")
        pref[input_list[inputlist][0]] = pref_mem_list

for inputlist in range(0, len(input_list)):

    if input_list[inputlist][3] == '_':
        non_pref[input_list[inputlist][0]] = []

    else:

        pref_mem_list = input_list[inputlist][3].split(",")
        non_pref[input_list[inputlist][0]] = pref_mem_list

# print()
# print()
# print(pref)
# print(non_pref)
# print(group_size)

members = list(pref.keys())
#print(members)
initial_teams = [set([member]) for member in members]
#print(initial_teams)

def cost_function(team):
    cost = k
    for member in team:
        if group_size[member] > 0 or group_size[member] != len(team):
            cost += 1
        common_pref = set(pref[member]).intersection(set(team))
        if len(pref[member]) - len(common_pref) > 0:
            cost += (len(pref[member]) - len(common_pref)) * n
        common_non_pref = set(non_pref[member]).intersection(set(team))
        if len(common_non_pref) > 0:
            cost += (len(common_non_pref)) * m
    return cost

q = Q.PriorityQueue()
for initial_team in initial_teams:
    team_cost = cost_function(initial_team)
    q.put((-team_cost, initial_team))

#print(q.queue)
total_cost = -sum([e[0] for e in q.queue])
#print(total_cost)

new_cost = 0

while(True):
    max_team = q.get()
    new_teams = Q.PriorityQueue()

    for team in q.queue:
        if len(team[1]) + len(max_team[1]) <= 3:
            candidate = [member for member in team[1]]
            candidate.extend(max_team[1])
            candidate_cost = cost_function(candidate)
            new_teams.put((candidate_cost, team))

    if new_teams.empty():
        q.put(max_team)
        break

    new_team_record = new_teams.get()
    new_team = [member for member in new_team_record[1][1]]
    new_team.extend(max_team[1])

    #print(new_team_record[1])
    new_total_cost = total_cost + new_team_record[1][0] + max_team[0] + new_team_record[0]
    #print(new_total_cost)
    if new_total_cost > total_cost:
        q.put(max_team)
        break
    q.queue.remove(new_team_record[1])
    q.put((-new_team_record[0], set(new_team)))
    #print(q.queue)
    total_cost = new_total_cost

for cost, team in q.queue:
    print(" ".join(team))
print(total_cost)