from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import sq, sq2, calc_distance


pyrimid_def = {
    'layer5': [
        (0,0,0), (sq,0,0), (2*sq,0,0), (3*sq,0,0), (4*sq,0,0),
        (0,sq,0), (sq,sq,0), (2*sq,sq,0), (3*sq,sq,0), (4*sq,sq,0),
        (0,2*sq,0), (sq,2*sq,0), (2*sq,2*sq,0), (3*sq,2*sq,0), (4*sq,2*sq,0),
        (0,3*sq,0), (sq,3*sq,0), (2*sq,3*sq,0), (3*sq,3*sq,0), (4*sq,3*sq,0),
        (0,4*sq,0), (sq,4*sq,0), (2*sq,4*sq,0), (3*sq,4*sq,0), (4*sq,4*sq,0),
        ],
    'layer4': [
        (sq2,sq2,1), (sq2+sq,sq2,1), (sq2+sq*2,sq2,1), (sq2+sq*3,sq2,1),
        (sq2,sq2+sq,1), (sq2+sq,sq2+sq,1), (sq2+sq*2,sq2+sq,1), (sq2+sq*3,sq2+sq,1),
        (sq2,sq2+2*sq,1), (sq2+sq,sq2+2*sq,1), (sq2+sq*2,sq2+2*sq,1), (sq2+sq*3,sq2+2*sq,1),
        (sq2,sq2+3*sq,1), (sq2+sq,sq2+3*sq,1), (sq2+sq*2,sq2+3*sq,1), (sq2+sq*3,sq2+3*sq,1),
    ],
    'layer3': [
        (sq,sq,2), (2*sq,sq,2), (3*sq,sq,2),
        (sq,2*sq,2), (2*sq,2*sq,2), (3*sq,2*sq,2),
        (sq,3*sq,2), (2*sq,3*sq,2), (3*sq,3*sq,2),
    ],
    'layer2': [
        (sq2+sq,sq2+sq,3), (sq2+sq*2,sq2+sq,3),
        (sq2+sq,sq2+2*sq,3), (sq2+sq*2,sq2+2*sq,3),
    ],
    'layer1': [
        (2*sq,2*sq,4)
    ],
}

def yield_pyrimid():
    n = 0
    for layer in pyrimid_def:
        for x, y, z in pyrimid_def[layer]:
            yield n, x, y, z
            n = n + 1


def check_one_layer(layer: int):
    xs = []
    ys = []
    for x, y, z in pyrimid_def['layer4']:
        xs.append(x)
        ys.append(y)
    plt.scatter(xs, ys)
    plt.show() 

def check_pyrimid():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for layer in pyrimid_def:
        for x, y, z in pyrimid_def[layer]:
            ax.scatter(x, y, z, c=z, alpha=1)

    plt.show()

position_dict = {n: (n, x, y, z) for n, x, y, z in yield_pyrimid()}
neighbor_dict = {0: {1, 5, 25}, 1: {0, 2, 6, 25, 26}, 5: {0, 6, 10, 25, 29}, 25: {0, 1, 5, 6, 41, 26, 29}, 2: {1, 3, 7, 26, 27}, 6: {1, 5, 7, 11, 25, 26, 29, 30}, 26: {1, 2, 6, 7, 41, 42, 25, 27, 30}, 3: {2, 4, 8, 27, 28}, 7: {2, 6, 8, 12, 26, 27, 30, 31}, 27: {2, 3, 7, 8, 42, 43, 26, 28, 31}, 4: {9, 3, 28}, 8: {32, 3, 7, 9, 13, 27, 28, 31}, 28: {32, 3, 4, 8, 9, 43, 27}, 9: {32, 4, 8, 14, 28}, 10: {33, 5, 11, 15, 29}, 29: {33, 5, 6, 41, 10, 11, 44, 25, 30}, 11: {33, 34, 6, 10, 12, 16, 29, 30}, 30: {34, 6, 7, 41, 42, 11, 12, 44, 45, 26, 29, 31}, 12: {34, 35, 7, 11, 13, 17, 30, 31}, 31: {32, 35, 7, 8, 42, 43, 12, 13, 45, 46, 27, 30}, 13: {32, 35, 36, 8, 12, 14, 18, 31}, 32: {36, 8, 9, 43, 13, 14, 46, 28, 31}, 14: {32, 36, 9, 13, 19}, 15: {33, 37, 10, 16, 20}, 33: {34, 37, 10, 11, 44, 15, 16, 47, 29}, 16: {33, 34, 37, 38, 11, 15, 17, 21}, 34: {33, 35, 38, 11, 12, 44, 45, 47, 16, 17, 48, 30}, 17: {34, 35, 38, 39, 12, 16, 18, 22}, 35: {34, 36, 39, 12, 13, 45, 46, 48, 17, 18, 49, 31}, 18: {35, 36, 39, 40, 13, 17, 19, 23}, 36: {32, 35, 40, 13, 14, 46, 49, 18, 19}, 19: {36, 40, 14, 18, 24}, 20: {37, 21, 15}, 37: {33, 38, 15, 16, 47, 20, 21}, 21: {37, 38, 16, 20, 22}, 38: {34, 37, 39, 47, 16, 17, 48, 21, 22}, 22: {38, 39, 17, 21, 23}, 39: {35, 38, 40, 48, 17, 18, 49, 22, 23}, 23: {39, 40, 18, 22, 24}, 40: {36, 39, 49, 18, 19, 23, 24}, 24: {40, 19, 23}, 41: {42, 44, 50, 25, 26, 29, 30}, 42: {41, 43, 45, 50, 51, 26, 27, 30, 31}, 43: {32, 42, 46, 51, 27, 28, 31}, 44: {33, 34, 41, 45, 47, 50, 52, 29, 30}, 45: {34, 35, 42, 44, 46, 48, 50, 51, 52, 53, 30, 31}, 46: {32, 35, 36, 43, 45, 49, 51, 53, 31}, 47: {33, 34, 37, 38, 44, 48, 52}, 48: {34, 35, 38, 39, 45, 47, 49, 52, 53}, 49: {35, 36, 39, 40, 46, 48, 53}, 50: {41, 42, 44, 45, 51, 52, 54}, 51: {42, 43, 45, 46, 50, 53, 54}, 52: {44, 45, 47, 48, 50, 53, 54}, 53: {45, 46, 48, 49, 51, 52, 54}, 54: {50, 51, 52, 53}}
    

if __name__ == '__main__':
    from itertools import combinations
    from collections import defaultdict
    distance_dict = {}
    neighbor_dict = defaultdict(set)
    for node1, node2 in combinations(yield_pyrimid(), 2):
        n1, x1, y1, z1 = node1
        n2, x2, y2, z2 = node2
        dist_ = calc_distance(node1, node2)
        distance_dict[(n1, n2)] = dist_
        if dist_ == 1.414:
            neighbor_dict[n1].add(n2)
            neighbor_dict[n2].add(n1)
        # break

    # print(distance_dict)

    print("desire pair", 55 * 54 / 2)
    print("distant_dict len:", len(distance_dict))
    print(neighbor_dict)
    print(position_dict)

    
    from collections import Counter
    distance_counter = Counter(distance_dict.values())
    print(sorted(distance_counter.keys()))
    print("total distance count", len(distance_counter.keys()))
        
