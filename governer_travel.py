import json
from math import radians, cos, sin, asin, sqrt
import copy

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c

def total_distance(route, coords):
    dist = 0
    for i in range(len(route) - 1):
        lat1, lon1 = coords[route[i]]
        lat2, lon2 = coords[route[i+1]]
        dist += haversine(lat1, lon1, lat2, lon2)
    return dist

def two_opt(route, coords):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                if total_distance(new_route, coords) < total_distance(best, coords):
                    best = new_route
                    improved = True
        route = best
    return best

with open('state_capitals_with_coordinates.json') as f:
    capitals = json.load(f)

capital_coords = {c['state']: (c['latitude'], c['longitude']) for c in capitals}

start, end = "Iowa", "Washington"
states_to_visit = set(capital_coords.keys()) - {start, end}

current = start
route = [start]

# Initial route with Nearest Neighbor
while states_to_visit:
    current = min(states_to_visit, key=lambda state: haversine(
        capital_coords[current][0], capital_coords[current][1],
        capital_coords[state][0], capital_coords[state][1]))
    route.append(current)
    states_to_visit.remove(current)

route.append(end)

# Optimize route using 2-opt
optimized_route = two_opt(route, capital_coords)

print("Optimized Route from Iowa to Washington:")
for state in optimized_route:
    print(state)
print("Total distance (km):", total_distance(optimized_route, capital_coords))
