from math import sqrt
from itertools import combinations
z_height = 1
sq = sqrt(2)
sq2 = sq / 2
radius = sq



def calc_distance(node1, node2):
    n1, x1, y1, z1 = node1
    n2, x2, y2, z2 = node2
    return round(sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2), 3)


def calc_fingerprint(brick):
    dist_pair = []
    for node1, node2 in combinations(brick, 2):
        dist_ = round(calc_distance(node1, node2), 3)
        dist_pair.append(dist_)
        
    dist_pair = sorted(dist_pair)
    return dist_pair
