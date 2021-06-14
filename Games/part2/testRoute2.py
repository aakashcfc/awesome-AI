#!/usr/local/bin/python3
# route.py : Road Trip!
#
# Code by: [Sri Harsha Manjunath - srmanj; Vijaylakshmi Maigur - vbmaigur; Disha Talreja - dtalreja]
#
#
#
# put your routing program here!

import sys
import numpy as np
from queue import PriorityQueue

# https://stackoverflow.com/questions/45491931/alternatives-for-defaultdict/45492139
## --- Beginning of code from the above link ---
# This code segments helps to append (new) items into the dictionary with unseen keys
def newkey(default_type):
    class Dict(dict):
        def __getitem__(self, key):
            if key not in self:
                dict.__setitem__(self, key, default_type())
            return dict.__getitem__(self, key)
    return Dict()
## --- End of code from the above link ---

def successor(city):
    ret_list = []
    for c in roads[city]:
        c = c.split("~")
        ret_list.append((1,c[1],c[4],np.round(float(c[1])/float(c[5]),2),c[5],c[0]))
    return ret_list


def solve(start_city,end_city,metric):
    visited = []
    fringe = PriorityQueue()
    fringe.put((0,0,0,0,0,0,"",start_city)) #[Priority][total-segments][total-miles][total-hours][total-gas-gallons][cities][cur-city]

    if metric == 'distance': #Return the least distant neighbor
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))
                if city not in visited:
                    tmp = float(tot_mil) + float(mil)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                            float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)

    elif metric == 'time': #Return the least time consuming neighbor
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))
                if city not in visited:
                    tmp = float(tot_hor) + float(hor)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                            float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)

    elif metric == 'mpg': #Return the cheapest neighbor in terms of mpg
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable
            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))
                if city not in visited:
                    tmp = float(tot_gal) + float(gal)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                        float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)

    else:#Return the least distant neighbor in terms of segments
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))

                if city not in visited:
                    tmp = float(tot_seg) + float(seg)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                            float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)
    return False


if __name__ == "__main__":
    '''if(len(sys.argv) != 4):
        raise(Exception("Error: expected 3 arguments"))'''

    #This scripts assumes the file road-segments.txt is available in the same directory
    road_segments = open("D:\\SEM-1\\ElementsOfAI\\asarnoba-deelango-sk128-a1-master\\part2\\"
                                               "road-segments.txt", 'r')
    roads = newkey(list) #Variable to store processed road segments

    #Process the road-segments.txt file
    for line in road_segments:
        everything = line.split(" ")

        city_a = everything[0].strip(); city_a.replace("\"","")
        city_b = everything[1].strip(); city_b.replace("\"","")
        dist = everything[2].strip()
        speed = everything[3].strip()
        time = int(dist)/int(speed)
        mpg = 400*(int(speed)/150) * (1-(int(speed)/150))**4
        h_name = everything[4].strip()

        #Creating the dictionary
        roads[city_a].append(city_b+"~"+dist+"~"+speed+"~"+h_name+"~"+str(np.round(time,3))+"~"+str(np.round(mpg,3)))
        roads[city_b].append(city_a+"~"+dist+"~"+speed+"~"+h_name+"~"+str(np.round(time,3))+"~"+str(np.round(mpg,3)))
        #This ensures that all streets are entered as a 2 way streets

    '''start_city = sys.argv[1]
    end_city = sys.argv[2]
    metric = sys.argv[3]'''
    start_city = "Bloomington,_Indiana"
    end_city = "Indianapolis,_Indiana"
    metric = "segments"

    result = solve(start_city,end_city,metric)

    if result == False:
        print("Inf")
    else:
        print(int(result[0]), int(result[1]), result[2], result[3],result[4].replace('[','').replace(']',' '))