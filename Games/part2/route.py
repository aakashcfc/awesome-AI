#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import heapq
from pprint import pprint
import sys
from math import sqrt,radians,cos,sin,asin
class Route:
    def __init__(self, segments_data, gps_data):
        self.segments = segments_data
        self.gps = gps_data
        self.approximate_distance_between_cities = {}

    def successors(self,city):          #return possible cities
        return self.segments[city].keys()


def calculate_distance( current_city, end_city , route):
        if current_city not in route.gps.keys() or end_city not in route.gps.keys():
            return 0
        city_pair = tuple(sorted((current_city, end_city)))
        #return route.approximate_distance_between_cities.get(city_pair,euclidean_distance(route.gps[current_city], route.gps[end_city]))
        return route.approximate_distance_between_cities.get(city_pair, haversineDistance(route.gps[current_city], route.gps[end_city]))

def euclidean_distance(coord1, coord2):
        x1,y1 = coord1
        x2,y2 = coord2
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


#used formula from wikipedia for haversine distance
def haversineDistance(x, y):
    lat1, lon1 = x
    lat2, lon2 = y
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    differencelon = lon2 - lon1
    differencelat = lat2 - lat1
    a = sin(differencelat / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(differencelon / 2.0) ** 2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles 3956 for miles
    return c * r

def load_segments( filename):
    road_segments = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            segments = line.split()
            city_a = segments[0]
            city_b = segments[1]
            if not road_segments.get(city_a, None):
                road_segments[city_a] = {}
            if not road_segments.get(city_b, None):
                road_segments[city_b] = {}
            # Adding it both ways
            road_segments[city_a][city_b] = (float(segments[2]), float(segments[3]), segments[4])
            road_segments[city_b][city_a] = (float(segments[2]), float(segments[3]), segments[4])
    return road_segments


def calculate_priority_cost( cost_function, end_city, present_state,segments,route):
        route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, accidents_so_far = present_state
        current_city = route_so_far[-1]

        if cost_function == "distance":
            distance_to_cover = calculate_distance(current_city, end_city,route)
            return miles_so_far + distance_to_cover
        if cost_function == "time":
            distance_to_cover = calculate_distance(current_city, end_city,route)
            max_speed = 65
            time_required_to_destination = distance_to_cover / max_speed
            return time_elapsed_so_far + time_required_to_destination
        if cost_function == "safe":
            accidents_count = calculate_accidents1(current_city,end_city,segments,route,present_state)
            return accidents_so_far + accidents_count
        return segments_so_far + 1

def calculate_accidents1(source , end_city , segments ,route ,present_state):

    all_accident_costs = {}
    route_till_now = present_state[0]

    for possible_route in segments[source]:
        route_dist = calculate_distance(source,possible_route,route)
        accidents_in_route = (route_dist / 1000000) if segments[source][possible_route][2][0] == 'I-' else 2 *((route_dist / 1000000))
        all_accident_costs[possible_route] = accidents_in_route

    min_cost = min(all_accident_costs.values())
    route_min_cost = [key for key in all_accident_costs if all_accident_costs[key] == min_cost]

    total_accidents_in_route_till_now =  all_accident_costs[route_min_cost[0]]
    return total_accidents_in_route_till_now


def calculate_accidents(segments ,route ,route_till_now):
    accidents_so_far = 0
    all_accident_costs = {}
    #accidents_so_far = present_state[-1]
    for i in range(0,len(route_till_now)-1) :
        a= route_till_now[i]
        b=route_till_now[i+1]
        previous_dist = calculate_distance(route_till_now[i], route_till_now[i+1], route)
        accidents_so_far += (previous_dist / 1000000) if segments[route_till_now[i+1]][route_till_now[i]][2][0] == 'I-' else 2 *((previous_dist / 1000000))

    return  accidents_so_far

def load_gps_data( filename):
    locations = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            gps_data = line.split()
            city = gps_data[0]
            latitude = float(gps_data[1])
            longitude = float(gps_data[2])
            locations[city] = (latitude, longitude)
    return locations

def get_route( start, end_city, cost_function):
        """
        Find shortest driving route between start city and end city
        based on a cost function.
        1. Your function should return a dictionary having the following keys:
            -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
               next-stop is a string giving the next stop in the route, and segment-info is a free-form
               string containing information about the segment that will be displayed to the user.
               (segment-info is not inspected by the automatic testing program).
            -"total-segments": an integer indicating number of segments in the route-taken
            -"total-miles": a float indicating total number of miles in the route-taken
            -"total-hours": a float indicating total amount of time in the route-taken
            -"total-expected-accidents": a float indicating the expected accident count on the route taken
        2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
        3. Please do not use any global variables, as it may cause the testing code to fail.
        4. You can assume that all test cases will be solvable.
        5. The current code just returns a dummy solution.
        """
        # segments = load_segments(filename="D:\\SEM-1\\ElementsOfAI\\asarnoba-deelango-sk128-a1-master\\part2\\"
        #                                        "road-segments.txt")
        segments = load_segments(filename="//u//asarnoba//asarnoba-deelango-sk128-a1//part2//road-segments.txt")
        gps_data = load_gps_data("//u//asarnoba//asarnoba-deelango-sk128-a1//part2//city-gps.txt")
        route = Route(segments, gps_data)
        fringe, route_so_far = [], [start]
        visited = {}                #visited cities
        priority_index_when_visited = {}
        segments_so_far, miles_so_far, time_elapsed_so_far,accidents_so_far = 0,0,0,0
        initial_fringe_element = (route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, accidents_so_far)
        priority_index = calculate_priority_cost(cost_function, end_city, initial_fringe_element,segments,route)
        heapq.heappush(fringe, (priority_index, initial_fringe_element))

        while fringe:
            priority_index, (
                route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, accidents_so_far) = heapq.heappop(
                fringe)

            source = route_so_far[-1]
            route_pairs = [(route_so_far[l+1], segments[route_so_far[l]][route_so_far[l+1]][2] + " for " + \
                            str(int(segments[route_so_far[l]][route_so_far[l+1]][0])) + " miles")
                           for l in range(len(route_so_far) - 1)]

            if source == end_city:
                route_pairs
                accidents_so_far = calculate_accidents(segments, route, route_so_far)
                return {"route-taken" : route_pairs, "total-miles" : miles_so_far, "total-segments" : segments_so_far,
                        "total-hours" : time_elapsed_so_far, "total-expected-accidents" : float(accidents_so_far)}
            # Mark the city as visited and note down the priority
            visited[source] = True
            priority_index_when_visited[source] = priority_index
            # Generate successors
            next_cities = Route.successors(route,  source)    #get next possible cities
            for city in next_cities:
                miles_to_city, speed_limit_on_highway, _ = segments[source][city]
                time_to_city = miles_to_city / speed_limit_on_highway
                #gallons_to_city = self.gas_gallons(miles_to_city, speed_limit_on_highway)

                next_fringe_element = (
                    route_so_far + [city], miles_so_far + miles_to_city, segments_so_far + 1,
                    time_elapsed_so_far + time_to_city, accidents_so_far)
                accidents_so_far = calculate_accidents(segments, route, route_so_far)

                next_fringe_element = (
                    route_so_far + [city], miles_so_far + miles_to_city, segments_so_far + 1,
                    time_elapsed_so_far + time_to_city, accidents_so_far)

                priority_value = calculate_priority_cost(cost_function, end_city, next_fringe_element,segments,route)

                visited_cities = visited.get(city, False)

                if visited_cities and float(priority_index) < float(priority_index_when_visited[
                    city]) and cost_function != "segments":
                    visited[city] = False
                    heapq.heappush(fringe, (priority_value, next_fringe_element))
                if not visited_cities:
                    heapq.heappush(fringe, (priority_value, next_fringe_element))
        return None


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print(" Then go to %s via %s" % step)

    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])