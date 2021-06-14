#!/usr/local/bin/python3

# put your routing program here!

import heapq
from math import sqrt
import sys


class RouteFinder:
    def __init__(self, segments_data, gps_data):
        self.segments = segments_data
        self.gps = gps_data
        self.approximate_distance_between_cities = {}

    @staticmethod
    def euclidean_distance(coord1, coord2):
        x1,y1 = coord1
        x2,y2 = coord2
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Formula for MPG: (400*speed/150) * (1-speed/150)^4
    def find_mpg(self, speed):
        return (400 * speed / 150) * (1 - speed / 150) ** 4

    # Gas gallons = Distance covered/MPG
    def gas_gallons(self, distance, speed):
        mpg = self.find_mpg(speed)
        return distance / mpg

    def successors(self, city):
        return self.segments[city].keys()

    # TODO: Need to handle cases of missing GPS co-ordinates. Currently returns 0
    def distance_between_cities(self, city1, city2):
        if city1 not in self.gps.keys() or city2 not in self.gps.keys():
            return 0
        city_pair = tuple(sorted((city1, city2)))
        return self.approximate_distance_between_cities.get(city_pair, self.euclidean_distance(self.gps[city1], self.gps[city2]))

    # TODO: A better cost function for segments?
    def get_priority_index(self, cost_function, end_city, present_state_of_search):
        route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, gallons_so_far = present_state_of_search
        current_city = route_so_far[-1]
        if cost_function == "distance":
            distance_to_cover = self.distance_between_cities(current_city, end_city)
            return miles_so_far + distance_to_cover
        if cost_function == "time":
            distance_to_cover = self.distance_between_cities(current_city, end_city)
            max_speed = 65
            time_required_to_destination = distance_to_cover / max_speed
            return time_elapsed_so_far + time_required_to_destination
        if cost_function == "mpg":
            distance_to_cover = self.distance_between_cities(current_city, end_city)
            max_speed = 65
            gallons_to_destination = self.gas_gallons(distance_to_cover, max_speed)
            return gallons_so_far + gallons_to_destination
        return segments_so_far + 1

    def find_route(self, start_city, end_city, cost_function):
        fringe, route_so_far = [], [start_city]
        visited = {}
        priority_index_when_visited = {}
        segments_so_far, miles_so_far, time_elapsed_so_far, gallons_so_far = 0, 0, 0, 0
        initial_fringe_element = (route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, gallons_so_far)
        priority_index = self.get_priority_index(cost_function, end_city, initial_fringe_element)
        heapq.heappush(fringe, (priority_index, initial_fringe_element))
        while fringe:
            priority_index, (
                route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, gallons_so_far) = heapq.heappop(
                fringe)
            source = route_so_far[-1]
            if source == end_city:
                return route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, gallons_so_far
            # Mark the city as visited and note down the priority
            visited[source] = True
            priority_index_when_visited[source] = priority_index
            # Generate successors
            next_cities = self.successors(source)
            for city in next_cities:
                miles_to_city, speed_limit_on_highway, _ = self.segments[source][city]
                time_to_city = miles_to_city / speed_limit_on_highway
                gallons_to_city = self.gas_gallons(miles_to_city, speed_limit_on_highway)
                next_fringe_element = (
                    route_so_far + [city], miles_so_far + miles_to_city, segments_so_far + 1,
                    time_elapsed_so_far + time_to_city, gallons_so_far + gallons_to_city)


                priority_index = self.get_priority_index(cost_function, end_city, next_fringe_element)
                has_city_been_visited = visited.get(city, False)

                if has_city_been_visited and priority_index < priority_index_when_visited[city] and cost_function != "segments":
                    visited[city] = False
                    heapq.heappush(fringe, (priority_index, next_fringe_element))
                if not has_city_been_visited:
                    heapq.heappush(fringe, (priority_index, next_fringe_element))
        return None


# Helper Methods
# Road segments format : CityA -> CityB -> (Length, SpeedLimit, HighwayName)
def load_road_segments(filename):
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


def load_gps(filename):
    locations = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            gps_data = line.split()
            city = gps_data[0]
            latitude = float(gps_data[1])
            longitude = float(gps_data[2])
            locations[city] = (latitude, longitude)
    return locations


if __name__ == "__main__":
    '''if len(sys.argv) != 4:
        raise (Exception("Expected 3 arguments. Got {}".format(len(sys.argv) - 1)))
    start_city = sys.argv[1]
    end_city = sys.argv[2]
    cost_function = sys.argv[3]'''
    ( start_city, end_city, cost_function) = ("Bloomington,_Indiana", "Indianapolis,_Indiana", "segments")
    if cost_function not in ["segments", "distance", "time", "mpg"]:
        raise (Exception("Unknown cost function encountered"))
    segments = load_road_segments("D:\\SEM-1\\ElementsOfAI\\asarnoba-deelango-sk128-a1-master\\part2\\road-segments.txt")
    gps_data = load_gps("D:\\SEM-1\\ElementsOfAI\\asarnoba-deelango-sk128-a1-master\\part2\\city-gps.txt")
    route_finder = RouteFinder(segments, gps_data)
    solution = route_finder.find_route(start_city, end_city, cost_function)
    if solution is None:
        print("Inf")
    else:
        route_so_far, miles_so_far, segments_so_far, time_elapsed_so_far, gallons_so_far = solution
        print("\n".join(["Take {} from {} to {} for {} miles".format(segments[route][route_so_far[index + 1]][2], route,
                                                                     route_so_far[index + 1],
                                                                     segments[route][route_so_far[index + 1]][0]) for
                         index, route in enumerate(route_so_far[:-1])]))
        print(
            "{} {} {} {} {}".format(segments_so_far, int(miles_so_far), round(time_elapsed_so_far, 4),
                                    round(gallons_so_far, 4),
                                    " ".join(route_so_far)))