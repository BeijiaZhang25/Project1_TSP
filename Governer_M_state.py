import json
from geopy.distance import geodesic
from itertools import permutations
from tqdm import tqdm

# 1. Load your JSON data
with open('state_capitals_structured_Hetong_Wang.json', 'r') as f:
    data = json.load(f)

# 2. Build a mapping from state name to (lat, lon)
state_coords = {entry['state']: (entry['latitude'], entry['longitude']) for entry in data}
print(state_coords.keys())
# 3. List your start, end, and "M" states
start = 'Iowa'
end = 'Washington DC'  # DC's state name in most datasets, or use 'Washington DC' if that's your key

# List of the eight "M" states, must match the exact 'state' key in the JSON
M_states = [
    'Maine',
    'Minnesota',
    'Maryland',
    'Mississippi',
    'Massachusetts',
    'Missouri',
    'Michigan',
    'Montana'
]

# 4. Brute-force search all permutations
min_distance = float('inf')
best_route = None

for route in tqdm(permutations(M_states), total=40320):
    # Build the route: start -> permuted "M" states -> end
    path = [start] + list(route) + [end]
    total_dist = 0
    for i in range(len(path) - 1):
        city1 = state_coords[path[i]]
        city2 = state_coords[path[i + 1]]
        total_dist += geodesic(city1, city2).kilometers
    if total_dist < min_distance:
        min_distance = total_dist
        best_route = path

# 5. Print the best route
print("Shortest route found:")
for loc in best_route:
    print(f"  {loc}")
print(f"Total distance: {min_distance:.2f} km")
