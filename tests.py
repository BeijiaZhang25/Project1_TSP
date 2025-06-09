import pytest

from main import held_karp, DistanceMatrixObject


def test_held_karp():

    # The following code should give you the min path of 2 -> 3 -> 1 -> 0 which is 65 using held_karp
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    distance_object: DistanceMatrixObject = {"distance_matrix": distance_matrix, "start_index": 2, "end_index": 0}
    min_distance = 65
    assert held_karp(distance_object) == min_distance, f"Held_Karp gives answer {held_karp(distance_object)} instead of {min_distance}"

def test_validation_of_held_karp_size():

    # Verify that distance matrix has a size of n x n.
    distance_matrix = [
        [0, 1, 2],
        [0, 1, 2],
    ]

    distance_object: DistanceMatrixObject = {"distance_matrix": distance_matrix, "start_index": 2, "end_index": 0}
    with pytest.raises(ValueError) as executable_info:
        held_karp(distance_object)

    assert str(executable_info.value) == "Matrix is not a square", "Held Karp ran smoothly while it was not a square"

def test_held_karp_distance_matrix_with_zero_length():
    distance_matrix = []
    distance_object: DistanceMatrixObject = {"distance_matrix": distance_matrix, "start_index": 2, "end_index": 0}

    assert held_karp(distance_object) == 0, f"Held Karp should return 0, instead it returned {held_karp(distance_object)}"