


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
