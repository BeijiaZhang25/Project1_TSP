import json
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import matplotlib.pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def create_distance_matrix(coords, city_list):
    size = len(city_list)
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                lat1, lon1 = coords[city_list[i]]
                lat2, lon2 = coords[city_list[j]]
                matrix[i][j] = int(haversine(lat1, lon1, lat2, lon2) * 1000)  # in meters
    return matrix

def main():
    with open("./state_capitals_structured_Hetong_Wang.json", "r") as f:
        data = json.load(f)

    city_names = [item["capital"] for item in data]
    coords = {item["capital"]: (item["latitude"], item["longitude"]) for item in data}

    # Index of start and end cities
    start_city = "Des Moines"
    end_city = "Washington"
    start_index = city_names.index(start_city)
    end_index = city_names.index(end_city)

    # Distance matrix
    dist_matrix = create_distance_matrix(coords, city_names)

    # OR-Tools setup
    manager = pywrapcp.RoutingIndexManager(len(dist_matrix), 1, [start_index], [end_index])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_idx, to_idx):
        from_node = manager.IndexToNode(from_idx)
        to_node = manager.IndexToNode(to_idx)
        return dist_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add constraint: end at a fixed node
    #routing.AddVariableMinimizedByFinalizer(routing.NextVar(manager.NodeToIndex(end_index)))

    # Solve
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_params)
    if not solution:
        print("No solution found.")
        return

    # Extract path
    index = routing.Start(0)
    route = []
    total_distance = 0
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(node)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))

    # Output
    print("Optimal route:")
    for i, idx in enumerate(route):
        print(f"{i + 1}. {city_names[idx]}")
    print(f"\nTotal distance: {total_distance / 1000:.2f} km")

    # Plot route
    plt.figure(figsize=(12, 8))
    for i in range(len(route) - 1):
        city1 = city_names[route[i]]
        city2 = city_names[route[i + 1]]
        plt.plot([coords[city1][1], coords[city2][1]], [coords[city1][0], coords[city2][0]], 'b-')
    for name in city_names:
        plt.plot(coords[name][1], coords[name][0], 'ro')
        plt.text(coords[name][1], coords[name][0], name, fontsize=7)
    plt.title("State Capitals TSP with OR-Tools")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.savefig("tsp_ortools_route.png")
    plt.close()

if __name__ == "__main__":
    main()
