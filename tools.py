import numpy as np


def angle_between(vector_1, vector_2, unit="rad"):
    angle_rad = np.arccos(np.clip(np.dot(unit_vector(vector_1), unit_vector(vector_2)), -1.0, 1.0))
    if unit == "rad":
        return angle_rad
    elif unit == "degree":
        return np.degrees(angle_rad)
    else:
        raise ValueError
    

def distance(pos_1, pos_2):
    if isinstance(pos_1, list):
        pos_1 = np.array(pos_1)
    if isinstance(pos_2, list):
        pos_2 = np.array(pos_2)
    return np.sqrt(np.sum(np.square(pos_2 - pos_1)))


def unit_vector(vector):
    if isinstance(vector, list):
        vector = np.array(vector)
    return vector / np.linalg.norm(vector)


if __name__ == "__main__":
    p1 = [0, 0]
    p2 = [3, 4]
    print(distance(p1, p2))