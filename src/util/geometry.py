import math
import numpy as np


def center_for_bounds(aabb):
    width = aabb[2] - aabb[0]
    height = aabb[3] - aabb[1]
    center_x = aabb[0] + width / 2
    center_y = aabb[1] + height / 2
    return (center_x, center_y)


def shapely_to_4x4_matrix(matrix):
    return np.append(np.array(matrix).reshape(
        (3, 4), order='F'), [0, 0, 0, 1]).reshape((4, 4), order='C')


def matrix_to_shapely(matrix):
    return tuple(matrix[:-1].flatten(order="F"))


def pointsEqual(pointA: list[int], pointB: list[int]):
    return math.isclose(pointA[0], pointB[0]) and math.isclose(pointA[1], pointB[1])


def angle_between(vector_1, vector_2):
    """
    Calculates the angle between two vectors in degrees, taken from https://www.adamsmith.haus/python/answers/how-to-get-the-angle-between-two-vectors-in-python.
    """

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)

    return np.degrees(angle)
