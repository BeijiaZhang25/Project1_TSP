import json
import math
from itertools import combinations

# --- Load JSON Data ---
with open("./state_capitals_with_coordinates.json", "r") as f:
    cities_data = json.load(f)

# --- Filter Cities ---
# Keep only capitals where the state name starts with 'M', plus start and end cities
filtered_data = []
for entry in cities_data:
    state = entry["state"]
    capital = entry["capital"]
    if state.startswith("M") or capital in ("Des Moines", "Olympia"):
        filtered_data.append(entry)

# --- Prepare City Info ---
cities = [entry["capital"] for entry in filtered_data]
coords = {entry["capital"]: (entry["latitude"], entry["longitude"]) for entry in filtered_data}
n = len(cities)
city_index = {city: idx for idx, city in enumerate(cities)}

# --- Haversine Distance Function ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# --- Build Distance Matrix ---
dist = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j:
            lat1, lon1 = coords[cities[i]]
            lat2, lon2 = coords[cities[j]]
            dist[i][j] = haversine(lat1, lon1, lat2, lon2)

# --- Held-Karp Algorithm for TSP with fixed start and end ---
def held_karp(start_name, end_name):
    start, end = city_index[start_name], city_index[end_name]
    dp = {}

    # Initialize base cases (start + one other node)
    for k in range(n):
        if k != start:
            dp[(1 << start) | (1 << k), k] = dist[start][k]

    # Main dynamic programming loop
    for subset_size in range(3, n + 1):
        for subset in combinations(range(n), subset_size):
            if start not in subset:
                continue
            bits = sum(1 << i for i in subset)
            for j in subset:
                if j == start:
                    continue
                prev_bits = bits & ~(1 << j)
                dp[(bits, j)] = min(
                    dp[(prev_bits, k)] + dist[k][j]
                    for k in subset if k != j and (prev_bits, k) in dp
                )

    # Final step: calculate min path cost ending at `end`
    full = (1 << n) - 1
    min_cost = min(
        dp[(full & ~(1 << end), k)] + dist[k][end]
        for k in range(n) if k != end and (full & ~(1 << end), k) in dp
    )
    return min_cost

# --- Run It ---
if __name__ == "__main__":
    result = held_karp("Des Moines", "Olympia")
    print(f"Minimum distance from Des Moines to all 'M' states ending at Olympia: {result:.2f} km")
