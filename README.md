# Project1_TSP


## Requirements

- Python 3.6 or higher
- uv


## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd projects
   ```

2. Install uv (If you haven't already):
   ```
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```

3. Install the required packages:
   ```
   uv add -r requirements.txt
   ```
4. Run the program
    ```
    uv run main.py
    ```

## Project 1 Documentation
1. Description:
    - Find the most efficient route (shortest total distance or time) for a politician to:
        - Visit every U.S. state capital exactly once
        - Start in Iowa
        - End in Washington, DC
2. Algorithm used: Held-Karp
    - Terminology Definition
        - j: represents the last city visited in a partial path
        - S: represents the set of visited cities
        - dp[S][j]: the minimum cost to reach city j after visiting all cities in set S(including j),starting from the Start city(Iowa).
    - Transition Formula
        - To compute dp[S][j], we look at all possible ways we could have arrived at city j
            - dp[S][j] = min{dp[S-{j}][k]+dist[k][j]} for all k in S -{j}
            - k: all cities k that are in S but not j
            - Explanation: S = {A, B, C}
                - In terms of dp[{A,B,C}][C], we need to consider:
                    - From A to C: dp[{A,B}][A] + dist(A, C)
                    - From B to C: dp[{A,B}][B] + dist(B, C)
                - dp[{A,B,C}][C] = min(
                            dp[{A,B}][A] + dist(A,C),
                            dp[{A,B}][B] + dist(B,C)
                        )
    - Pseudocode
        - Input:
            - cities: list of all 50 U.S state capitals
            - dist[i][j]: pairwise distances between cities
            - start_city: "Des Moines"
            - end_city: "Washington"
        - Preprocessing:
            - Map city names to indices (0,n-1)
            - Let start = index of "Des Moines"
            - Let end = index of "Washington"
            - Let n = total number of cities
        - Initialize for start city:
            ```
            dp = dict()
            For all cities j ≠ start:
                subset = bitmask including start and j
                dp[(subset, j)] = dist[start][j]
            ```
        - Main:
            ```
            For subset_size from 3 to n:
                For all subsets S of size subset_size that include start:
                    For all j in S, j ≠ start:
                        dp[(S, j)] = min(
                        dp[(S - {j}, k)] + dist[k][j]
                        for all k in S - {j}
                )
            ```
        - Final step:
            - To fix the end city:
                ```
                result = min(
                    dp[(AllCities, end)]
                )
                ```
    - Time complexity: $O(n^2 * 2^n)$

## main.py
    - Output: Minimum distance from Des Moines to all 'M' states ending at Olympia: 7583.77 km

