from collections import defaultdict
from pyrimid_def import pyrimid_def, neighbor_dict, position_dict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import pickle
with open('brick_possible_pos.pkl', 'rb') as f:
    result = pickle.load(f)


def plot_brick_possible_position():
    # Create a 2x2 grid of 3D plots
    fig = plt.figure(figsize=(20, 20))

    # Plot 16 different views of the result['A'] positions
    for i in range(16):
        ax = fig.add_subplot(4, 4, i+1, projection='3d')
        
        # Plot all pyramid points in blue
        for layer in pyrimid_def:
            for x, y, z in pyrimid_def[layer]:
                ax.scatter(x, y, z, c='blue', alpha=0.3)
                
        # Plot the specific result['A'] configuration in red
        nodes = result['F'][16+i]  # Get the i-th configuration
        for node_id in nodes:
            _, x, y, z = position_dict[node_id]
            ax.scatter(x, y, z, c='red', s=100)
            
        # Set viewing angle for each subplot
        ax.view_init(elev=30 + (i//4)*15, azim=45 + (i%4)*90)
        ax.set_title(f'Configuration {i+1}')

    plt.tight_layout()
    plt.show()


def get_available_pos_brick():
    pos_available_brick = defaultdict(set)
    print(result['A'])
    for brick, position_set in result.items():
        print(f"\nBrick {brick} can be placed in {len(position_set)} ways:")
        for position in position_set:
            for node_id in position:
                pos_available_brick[node_id].add(brick)

# pos_available_brick = get_available_pos_brick()
# print(pos_available_brick)

pos_available_brick = {0: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 1: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 2: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 3: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 5: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 10: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 15: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 25: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 41: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 50: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 4: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 6: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 11: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 16: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 26: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 42: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 51: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 7: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 12: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 17: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 8: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 13: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 18: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 27: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 9: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 14: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 19: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 28: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 43: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 20: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 29: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 44: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 52: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 21: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 30: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 45: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 53: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 22: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 23: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 31: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 32: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 46: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 24: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 33: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 34: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 35: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 37: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 47: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 36: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 38: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 48: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 40: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}, 49: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 39: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'I', 'K'}, 54: {'F', 'D', 'J', 'L', 'A', 'G', 'E', 'B', 'C', 'H', 'K'}}
# print(pos_available_brick)
if __name__ == '__main__':
    plot_brick_possible_position()
