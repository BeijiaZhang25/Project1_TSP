import json
import math
import numpy as np
from sklearn.cluster import KMeans
from itertools import combinations
import matplotlib.pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def build_distance_matrix(cities, coords):
    n = len(cities)
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                lat1, lon1 = coords[cities[i]]
                lat2, lon2 = coords[cities[j]]
                dist[i][j] = haversine(lat1, lon1, lat2, lon2)
    return dist

def nearest_neighbor_tsp(dist_matrix, start_idx, end_idx):
    n = len(dist_matrix)
    unvisited = set(range(n))
    unvisited.remove(start_idx)
    path = [start_idx]
    current = start_idx
    
    while unvisited:
        next_city = min(unvisited, key=lambda x: dist_matrix[current][x])
        path.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    
    # Ensure we end at the specified end city
    if end_idx != path[-1]:
        path.append(end_idx)
    
    return path

def solve_cluster_tsp(cluster_cities, coords, start_city=None, end_city=None):
    dist_matrix = build_distance_matrix(cluster_cities, coords)
    start_idx = cluster_cities.index(start_city) if start_city else 0
    end_idx = cluster_cities.index(end_city) if end_city else len(cluster_cities) - 1
    return nearest_neighbor_tsp(dist_matrix, start_idx, end_idx)



def main():
    # Load data
    with open("./state_capitals_with_coordinates.json", "r") as f:
        cities_data = json.load(f)
    
    # Extract coordinates and city names
    cities = [entry["capital"] for entry in cities_data]
    coords = {entry["capital"]: (entry["latitude"], entry["longitude"]) 
             for entry in cities_data}
    
    # Prepare data for clustering
    X = np.array([[coords[city][0], coords[city][1]] for city in cities])
    
    # Perform K-means clustering
    n_clusters = 5  # Adjust based on your needs
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    # Organize cities by cluster
    cluster_cities = [[] for _ in range(n_clusters)]
    for i, cluster in enumerate(clusters):
        cluster_cities[cluster].append(cities[i])
    
    # Find start and end clusters
    start_city = "Des Moines"
    end_city = "Washington"
    start_cluster = None
    end_cluster = None
    
    for i, cluster in enumerate(cluster_cities):
        if start_city in cluster:
            start_cluster = i
        if end_city in cluster:
            end_cluster = i
    
    # Solve TSP within each cluster
    cluster_paths = []
    for i, cluster in enumerate(cluster_cities):
        if i == start_cluster:
            path = solve_cluster_tsp(cluster, coords, start_city=start_city)
        elif i == end_cluster:
            path = solve_cluster_tsp(cluster, coords, end_city=end_city)
        else:
            path = solve_cluster_tsp(cluster, coords)
        cluster_paths.append([cluster[j] for j in path])

    #For each cluster:
    #If it's the start cluster, we ensure the path starts from Des Moines
    #If it's the end cluster, we ensure the path ends in Washington, DC
    #For other clusters, we find the optimal path without specific start/end points
    
    # Connect clusters
    final_path = []
    current_cluster = start_cluster
    
    while cluster_paths:
        final_path.extend(cluster_paths[current_cluster])
        cluster_paths.pop(current_cluster)
        
        if not cluster_paths:
            break
            
        # Find nearest cluster
        current_city = final_path[-1]
        min_dist = float('inf')
        next_cluster = None
        
        for i, cluster in enumerate(cluster_paths):
            for city in cluster:
                dist = haversine(coords[current_city][0], coords[current_city][1],
                               coords[city][0], coords[city][1])
                if dist < min_dist:
                    min_dist = dist
                    next_cluster = i
        
        current_cluster = next_cluster
    
    # Calculate total distance
    total_distance = 0
    for i in range(len(final_path) - 1):
        city1, city2 = final_path[i], final_path[i + 1]
        total_distance += haversine(coords[city1][0], coords[city1][1],
                                  coords[city2][0], coords[city2][1])
    
    print("Optimal route:")
    for i, city in enumerate(final_path):
        print(f"{i+1}. {city}")
    print(f"\nTotal distance: {total_distance:.2f} km")
    
    # Visualize the route
    plt.figure(figsize=(12, 8))
    for i in range(len(final_path) - 1):
        city1, city2 = final_path[i], final_path[i + 1]
        plt.plot([coords[city1][1], coords[city2][1]], 
                [coords[city1][0], coords[city2][0]], 'b-')
    
    # Plot cities
    for city in cities:
        plt.plot(coords[city][1], coords[city][0], 'ro')
        plt.text(coords[city][1], coords[city][0], city, fontsize=8)
    
    plt.title('State Capitals TSP Route')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig('tsp_route.png')
    plt.close()

if __name__ == "__main__":
    main()