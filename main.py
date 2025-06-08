import json
import math
from itertools import combinations
from typing import TypedDict, List


class Address(TypedDict):
    """
    An Address object formatted as a standardized address
    """
    street: str
    city: str
    state: str
    zip: str

class StateCapital(TypedDict):
    """
    A StateCapital object formatted for use of input in this program
    """
    state: str
    capital: str
    address: Address
    latitude: float
    longitude: float

class DistanceMatrixObject(TypedDict):
    """
    A Distance Matrix containing starting and ending index to be used for defined algorithms
    """
    distance_matrix: List[List[float]]
    start_index: int
    end_index: int

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Description:
    Uses Haversine Formula (https://en.wikipedia.org/wiki/Haversine_formula)
    to find the distance on Earth from two points geographically.

    Haversine Formula is:
    a = sin²(Δφ/2) + cos φ1 * cos φ2 * sin²(Δλ/2)
    c = 2 * atan2(√a, √(1−a))
    d = R * c
    Where:
    * φ is latitude in radians
    * λ is longitude in radians
    * R is Earth's radius in miles (3958.756)
    * Δφ is the difference in latitudes
    * Δλ is the difference in longitudes

    :param lat1: Point A latitude as a float.
    :param lon1: Point A longitude as a float.
    :param lat2: Point B latitude as a float.
    :param lon2: Point B longitude as a float.
    :return: Distance between Point A and Point B on the Earth as a float
    """
    radius_earth_miles = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return radius_earth_miles * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def held_karp(distance_matrix_json: DistanceMatrixObject) -> float:
    """
    Description:
    This uses the Held-Karp algorithm (https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm#:~:text=The%20Held%E2%80%93Karp%20algorithm,%20also,to%20find%20a%20minimum-length)
    to find the minimum path visiting all nodes only once, starting from a specified start node and ending at a specified end node.

    :param distance_matrix_json: A dictionary-object containing:
            - 'distance_matrix': 2D list/array where a distance_matrix[row][column] represents
               the distance from a node at that row to a node at that column
            - 'start_index': Integer index of the starting node
            - 'end_index': Integer index of the ending node
    :return: Minimum cost to visit all nodes exactly once, starting from the start_index and ending at the end_index.

    Notes:
    - Has time complexity O(n²2ⁿ) where n is the number of nodes
    - Has space complexity O(n2ⁿ)
    """
    distance_matrix = distance_matrix_json['distance_matrix']
    start = distance_matrix_json['start_index']
    end = distance_matrix_json['end_index']
    n = len(distance_matrix)
    dp = {}

    # Initialize base cases (start + one other node)
    for k in range(n):
        if k != start:
            dp[(1 << start) | (1 << k), k] = distance_matrix[start][k]

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
                    dp[(prev_bits, k)] + distance_matrix[k][j]
                    for k in subset if k != j and (prev_bits, k) in dp
                )

    # Final step: calculate min path cost ending at `end`
    full = (1 << n) - 1
    min_cost = min(
        dp[(full & ~(1 << end), k)] + distance_matrix[k][end]
        for k in range(n) if k != end and (full & ~(1 << end), k) in dp
    )
    return min_cost

def filter_state_capitals(state_capitals: List[StateCapital]) -> List[StateCapital]:
    """
    Filter the state capitals on a given method.

    Method: Returns cities starting with M or capitals containing Des Moines or Olympia.

    :param state_capitals: The list of state_capitals grabbed from the JSON.
    :return: The cities that were filtered using the method above.
    """
    filtered_state_capitals = []
    for state_capital in state_capitals:
        state = state_capital["state"]
        capital = state_capital["capital"]
        if state.startswith("M") or capital in ("Des Moines", "Olympia"):
            filtered_state_capitals.append(state_capital)

    return filtered_state_capitals

def create_distance_matrix_object(state_capitals: List[StateCapital], start_name: str, end_name: str) -> DistanceMatrixObject:
    """
    Description:
    The method uses state_capitals and creates a distance matrix out of the different distances from each state_capital.
    The method also converts the start_name and end_name into start_index and end_index to be used for the algorithms.

    :param state_capitals: Objects containing a list of State Capital data.
    :param start_name: The state capital where the algorithm should start.
    :param end_name: The state capital where the algorithm should end.
    :return: DistanceMatrixObject (Dictionary) that has the DistanceMatrix along with start_index and end_index
    """
    cities = [state_capital["capital"] for state_capital in state_capitals]
    coords = {state_capital["capital"]: (state_capital["latitude"], state_capital["longitude"]) for state_capital in state_capitals}
    n = len(cities)
    city_index = {city: idx for idx, city in enumerate(cities)}
    dist = [[0] * n for _ in range(n)]
    for row in range(n):
        for column in range(n):
            if row != column:
                lat1, lon1 = coords[cities[row]]
                lat2, lon2 = coords[cities[column]]
                dist[row][column] = haversine(lat1, lon1, lat2, lon2)

    start_index, end_index = city_index[start_name], city_index[end_name]
    return {"distance_matrix": dist, "start_index": start_index, "end_index": end_index}


if __name__ == "__main__":
    """
    Description:
    The program follows these steps:
    1.) Load State Capitals from a JSON file.
    2.) Filter State Capitals.
    3.) Create a Distance Matrix that also has starting point and ending point.
    4.) Print out the result.
    """

    with open("./state_capitals_with_coordinates.json", "r") as f:
        state_capitals_data = json.load(f)

    state_capitals = filter_state_capitals(state_capitals_data)
    distance_matrix_object = create_distance_matrix_object(state_capitals, "Des Moines", "Olympia")

    result = held_karp(distance_matrix_object)
    print(f"Minimum distance from Des Moines, Iowa to all 'M' states ending at Olympia, Washington: {result:.2f} miles")
