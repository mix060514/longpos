from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import sq, sq2, calc_distance,calc_fingerprint


"""
layer5 = [
        (0,0,0), (sq,0,0), (2*sq,0,0), (3*sq,0,0), (4*sq,0,0),
        (0,sq,0), (sq,sq,0), (2*sq,sq,0), (3*sq,sq,0), (4*sq,sq,0),
        (0,2*sq,0), (sq,2*sq,0), (2*sq,2*sq,0), (3*sq,2*sq,0), (4*sq,2*sq,0),
        (0,3*sq,0), (sq,3*sq,0), (2*sq,3*sq,0), (3*sq,3*sq,0), (4*sq,3*sq,0),
        (0,4*sq,0), (sq,4*sq,0), (2*sq,4*sq,0), (3*sq,4*sq,0), (4*sq,4*sq,0),

]
"""

brick_example = {
    'A': [
        (0,0,0), (sq,0,0), (2*sq,0,0), (3*sq,0,0),
    ],
    'B': [
        (0,0,0), (sq,0,0), (2*sq,0,0), (3*sq,0,0),
        (0,sq,0),
    ],
    'C': [
        (0,0,0), (sq,0,0), 
        (0,sq,0), (sq,sq,0), 
    ],
    'D': [
        (0,0,0), (sq,0,0), 
        (0,sq,0),
    ],
    'E': [
        (0,0,0), (sq,0,0), (2*sq,0,0),
        (0,sq,0), (sq,sq,0), 
    ],
    'F': [
        (0,0,0), (sq,0,0), (2*sq,0,0), (3*sq,0,0),
                 (sq,sq,0),
    ],
    'G': [
        (0,0,0), (sq,0,0),
                 (sq,sq,0), (2*sq,sq,0), (3*sq,sq,0),
    ],
    'H': [
        (0,0,0)            , (2*sq,0,0),
        (0,sq,0), (sq,sq,0), (2*sq,sq,0),
    ],
    'I': [
                  (sq,0,0), 
        (0,sq,0), (sq,sq,0), (2*sq,sq,0),
                  (sq,2*sq,0),
    ],
    'J': [
        (0,0,0), (sq,0,0), (2*sq,0,0),
        (0,sq,0),
    ],
    'K': [
        (0,0,0), (sq,0,0), (2*sq,0,0),
        (0,sq,0),
        (0,2*sq,0),
    ],
    'L': [
                  (sq,0,0), (2*sq,0,0),
        (0,sq,0), (sq,sq,0),
        (0,2*sq,0),
    ],
}

for brick in brick_example:
    for n, node in enumerate(brick_example[brick]):
        node = list(node)
        node.insert(0,n)
        node = tuple(node)
        brick_example[brick][n] = node

brick_fingerprint = {'A': [1.414, 1.414, 1.414, 2.828, 2.828, 4.243], 'B': [1.414, 1.414, 1.414, 1.414, 2.0, 2.828, 2.828, 3.162, 4.243, 4.472], 'C': [1.414, 1.414, 1.414, 1.414, 2.0, 2.0], 'D': [1.414, 1.414, 2.0], 'E': [1.414, 1.414, 1.414, 1.414, 1.414, 2.0, 2.0, 2.0, 2.828, 3.162], 'F': [1.414, 1.414, 1.414, 1.414, 2.0, 2.0, 2.828, 2.828, 3.162, 4.243], 'G': [1.414, 1.414, 1.414, 1.414, 2.0, 2.0, 2.828, 3.162, 3.162, 4.472], 'H': [1.414, 1.414, 1.414, 1.414, 2.0, 2.0, 2.828, 2.828, 3.162, 3.162], 'I': [1.414, 1.414, 1.414, 1.414, 2.0, 2.0, 2.0, 2.0, 2.828, 2.828], 'J': [1.414, 1.414, 1.414, 2.0, 2.828, 3.162], 'K': [1.414, 1.414, 1.414, 1.414, 2.0, 2.828, 2.828, 3.162, 3.162, 4.0], 'L': [1.414, 1.414, 1.414, 1.414, 2.0, 2.0, 2.0, 3.162, 3.162, 4.0]}

if __name__ == '__main__':
    print("total brick node count", sum([len(brick_example[brick]) for brick in brick_example]))

    fingerprint_dict = {}
    for brick in brick_example:
        print(brick, len(brick_example[brick]), ' should have', int(len(brick_example[brick]) * (len(brick_example[brick]) - 1) / 2), 'pair')
        fp_ = calc_fingerprint(brick_example[brick])
        fingerprint_dict[brick] = fp_
    print(fingerprint_dict)



