#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
from math import tanh

# returns lines with city
def get_fringe(city):
    nodes = []
    with open('road-segments.txt', 'r') as f:
        lines = f.readlines()
        for line in range(len(lines)):
            if lines[line][0: len(city)] == city:
                nodes.append(lines[line])
            split_line = lines[line].split()
            city2 = split_line[1]
            if city == city2:
                nodes.append(lines[line])
    return nodes

# gets desination, the origin argument states which city you are coming from
def get_destination(line, origin):
    split_line = line.split()
    if origin == split_line[1]:
        return split_line[0]
    return split_line[1]
            
# gets distance between two cities
def get_distance_two(city1, city2):
    with open('road-segments.txt', 'r') as f:
        lines = f.readlines()
        for line in range(len(lines)):
            split_line = lines[line].split()
            if city1 in split_line and city2 in split_line:
                return float(split_line[2])

# gets time between two cities
def get_time_two(city1, city2):
    with open('road-segments.txt', 'r') as f:
        lines = f.readlines()
        for line in range(len(lines)):
            split_line = lines[line].split()
            if city1 in split_line and city2 in split_line:
                return float(split_line[2]) / float(split_line[3])
            
# gets delivery time between two cities
def get_delivery_two(city1, city2, time):
    with open('road-segments.txt', 'r') as f:
        lines = f.readlines()
        for line in range(len(lines)):
            split_line = lines[line].split()
            if city1 in split_line and city2 in split_line:
                t = float(split_line[2]) / float(split_line[3])
                if int(split_line[3]) < 50:
                    return t
                else:
                    return t + tanh(float(split_line[2])/1000) * (2 * t + 2 * time)

# get highway between two cities
def get_highway(city1, city2):
    with open('road-segments.txt', 'r') as f:
        lines = f.readlines()
        for line in range(len(lines)):
            split_line = lines[line].split()
            if city1 in split_line and city2 in split_line:
                return split_line[4]

# get distance from line
def get_distance(line):
    split_line = line.split()
    return float(split_line[2])

# get time frome line
def get_time(line):
    split_line = line.split()
    return float(split_line[2]) / float(split_line[3])

# get delivery time from line
def get_delivery(line, prev_time):
    split_line = line.split()
    if int(split_line[3]) < 50:
        return get_time(line)
    else:
        return get_time(line) + tanh(get_distance(line)/1000) * (2 * get_time(line) + 2 * prev_time)
            
# Source: https://www.pythonpool.com/a-star-algorithm-python/
# helped me better understand the structure of a-star 
# gave me a good way to keep track of fringe/visited nodes using sets
def get_route(start, end, cost):
    # Key : City, Value : f
    segment_fringe = {}
    distance_fringe = {}
    time_fringe = {}
    delivery_fringe = {}
    
    # fringe and visited nodes
    fringe_nodes = set([start])
    visited_cities = set([])
    
    segment_fringe[start] = 0
    distance_fringe[start] = 0
    time_fringe[start] = 0
    delivery_fringe[start] = 0
    
    # keeps track of adjacent nodes
    hist = {}
    hist[start] = start
    
    # while there are nodes left to be expanded, continue
    while len(fringe_nodes) > 0:
        next_city = None
        
        # find next node to be expanded, based on appropriate cost
        if cost == "segments":
            for node in fringe_nodes:
                if next_city == None or segment_fringe[node] + 1 < segment_fringe[next_city] + 1:
                    next_city = node
        if cost == "distance":
            for node in fringe_nodes:
                if next_city == None or distance_fringe[node] + get_distance_two(node, hist[node]) < distance_fringe[next_city] + get_distance_two(next_city, hist[next_city]):
                    next_city = node
        if cost == "time":
            for node in fringe_nodes:
                if next_city == None or time_fringe[node] + get_time_two(node, hist[node]) < time_fringe[next_city] + get_time_two(next_city, hist[next_city]):
                    next_city = node
        if cost == "delivery":
            for node in fringe_nodes:
                if next_city == None or delivery_fringe[node] + get_delivery_two(node, hist[node], time_fringe[node]) < delivery_fringe[next_city] + get_delivery_two(next_city, hist[next_city], time_fringe[next_city]):
                    next_city = node
        
        # check goal state
        if next_city == end:
            
            # use hist to reconstruct path (idea taken from above source)
            reconst_path = []
            while hist[next_city] != next_city:
                reconst_path.append(next_city)
                next_city = hist[next_city]
            
            # use path to get route taken
            reconst_path.append(start)
            reconst_path.reverse()
            print(distance_fringe)
            route_taken = []
            for city in range(len(reconst_path)-1):
                city1 = reconst_path[city]
                city2 = reconst_path[city+1]
                miles = get_distance_two(city1, city2)
                highway = get_highway(city1, city2)
                seg = str(highway) + " for " + str(miles) + " miles"
                
                route_taken.append((city2, seg))
            
            # return dict
            return {"total-segments" : segment_fringe[end],
                    "total-miles" : distance_fringe[end],
                    "total-hours" : time_fringe[end], 
                    "total-delivery-hours" : delivery_fringe[end],
                    "route-taken" : route_taken}
        
        # get fringe, returns LINES not CITIES
        next_nodes = get_fringe(next_city)
        
        for node in range(len(next_nodes)):
            # gets actual city from line
            n = get_destination(next_nodes[node], next_city)
            # update fringe
            if n not in visited_cities and n not in fringe_nodes:
                fringe_nodes.add(n)
                hist[n] = next_city
                segment_fringe[n] = segment_fringe[next_city] + 1
                distance_fringe[n] = distance_fringe[next_city] + get_distance(next_nodes[node])
                time_fringe[n] = time_fringe[next_city] + get_time(next_nodes[node])
                delivery_fringe[n] = delivery_fringe[next_city] + get_delivery(next_nodes[node], time_fringe[next_city])
                
                if cost == "distance":
                    if distance_fringe[n] > distance_fringe[next_city] + get_distance(next_nodes[node]):
                        delivery_fringe[n] = delivery_fringe[next_city] + get_delivery(next_nodes[node], time_fringe[next_city])
                        time_fringe[n] = time_fringe[next_city] + get_time(next_nodes[node])
                        distance_fringe[n] = distance_fringe[next_city] + get_distance(next_nodes[node])
                        segment_fringe[n] = segment_fringe[next_city] + 1
                        hist[n] = next_city
                        
                        if n in visited_cities:
                            visited_cities.remove(n)
                            fringe_nodes.add(n)
                            
                if cost == "segment":
                    if segment_fringe[n] > segment_fringe[next_city] + 1:
                        delivery_fringe[n] = delivery_fringe[next_city] + get_delivery(next_nodes[node], time_fringe[next_city])
                        time_fringe[n] = time_fringe[next_city] + get_time(next_nodes[node])
                        distance_fringe[n] = distance_fringe[next_city] + get_distance(next_nodes[node])
                        segment_fringe[n] = segment_fringe[next_city] + 1
                        hist[n] = next_city
                        
                        if n in visited_cities:
                            visited_cities.remove(n)
                            fringe_nodes.add(n)
                            
                if cost == "time":
                    if time_fringe[n] > time_fringe[next_city] + get_time(next_nodes[node]):
                        delivery_fringe[n] = delivery_fringe[next_city] + get_delivery(next_nodes[node], time_fringe[next_city])
                        time_fringe[n] = time_fringe[next_city] + get_time(next_nodes[node])
                        distance_fringe[n] = distance_fringe[next_city] + get_distance(next_nodes[node])
                        segment_fringe[n] = segment_fringe[next_city] + 1
                        hist[n] = next_city
                        
                        if n in visited_cities:
                            visited_cities.remove(n)
                            fringe_nodes.add(n)
                            
                if cost == "delivery":
                    if delivery_fringe[n] > delivery_fringe[next_city] + get_delivery(next_nodes[node], time_fringe[next_city]):
                        delivery_fringe[n] = delivery_fringe[next_city] + get_delivery(next_nodes[node], time_fringe[next_city])
                        time_fringe[n] = time_fringe[next_city] + get_time(next_nodes[node])
                        distance_fringe[n] = distance_fringe[next_city] + get_distance(next_nodes[node])
                        segment_fringe[n] = segment_fringe[next_city] + 1
                        hist[n] = next_city
                
                        if n in visited_cities:
                            visited_cities.remove(n)
                            fringe_nodes.add(n)
                            
        # remove visited node from fringe, add to visited cities
        fringe_nodes.remove(next_city)
        visited_cities.add(next_city)
    return None

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


