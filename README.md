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

3. Create a virtual environment within the repository and activate it:
   ```
   uv venv .venv
   ```
   
4. Install the required packages:
   ```
   uv pip install -r requirements.txt
   ```
   
5. Run the program
   ```
    uv run main.py
   ```

## Project 1 Documentation
1. Description:
    - Find the most efficient route (shortest total distance or time) for a politician to:
        - Visit every U.S. state capital exactly once
        - Start in Iowa
        - End in Washington
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

## tsp_ortoolspy
    - Output:
        Optimal route:
            1. Des Moines
            2. Saint Paul
            3. Bismarck
            4. Pierre
            5. Cheyenne
            6. Denver
            7. Salt Lake City
            8. Helena
            9. Boise
            10. Salem
            11. Olympia
            12. Juneau
            13. Honolulu
            14. Sacramento
            15. Carson City
            16. Phoenix
            17. Santa Fe
            18. Austin
            19. Baton Rouge
            20. Jackson
            21. Montgomery
            22. Tallahassee
            23. Atlanta
            24. Columbia
            25. Raleigh
            26. Richmond
            27. Charleston
            28. Columbus
            29. Indianapolis
            30. Frankfort
            31. Nashville
            32. Little Rock
            33. Oklahoma City
            34. Topeka
            35. Lincoln
            36. Jefferson City
            37. Springfield
            38. Madison
            39. Lansing
            40. Harrisburg
            41. Albany
            42. Montpelier
            43. Augusta
            44. Concord
            45. Boston
            46. Providence
            47. Hartford
            48. Trenton
            49. Dover
            50. Annapolis
            51. Washington
        Total distance: 26734.95 km
    - tsp_ortools_route.png
   Hetong output:
      Iowa
      Nebraska
      Kansas
      Missouri
      Illinois
      Indiana
      Kentucky
      Ohio
      West Virginia
      Virginia
      North Carolina
      South Carolina
      Florida
      Alabama
      Georgia
      Tennessee
      Mississippi
      Louisiana
      Arkansas
      Oklahoma
      Texas
      New Mexico
      Arizona
      Nevada
      California
      Hawaii
      Alaska
      Washington
      Oregon
      Idaho
      Montana
      Utah
      Colorado
      Wyoming
      South Dakota
      North Dakota
      Minnesota
      Wisconsin
      Michigan
      Vermont
      Maine
      New Hampshire
      Massachusetts
      Rhode Island
      Connecticut
      New York
      New Jersey
      Pennsylvania
      Delaware
      Maryland
      Washington DC
      Total distance (miles): 16553.32
