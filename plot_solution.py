"""
Found a solution!
Brick I: [11, 15, 16, 17, 21]
Brick A: [20, 37, 47, 52]
Brick E: [0, 1, 5, 6, 10]
Brick L: [14, 18, 22, 36, 39]
Brick D: [19, 23, 24]
Brick B: [40, 49, 50, 53, 54]
Brick G: [9, 32, 35, 46, 48]
Brick C: [41, 42, 44, 45]
Brick K: [25, 26, 27, 29, 33]
Brick J: [30, 31, 34, 38]
Brick H: [2, 3, 7, 12, 13]
Brick F: [4, 8, 28, 43, 51]
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from pyrimid_def import position_dict
import pickle

def plot_solution(solution):
    """
    Plot the solution with different colors for each brick
    """
    # 設置顏色映射
    colors = {
        'A': 'red',
        'B': 'blue',
        'C': 'green',
        'D': 'yellow',
        'E': 'purple',
        'F': 'orange',
        'G': 'pink',
        'H': 'cyan',
        'I': 'magenta',
        'J': 'brown',
        'K': 'gray',
        'L': 'olive'
    }

    # 創建3D圖
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')

    # 繪製每個積木
    for brick, positions in solution:
        for node_id in positions:
            _, x, y, z = position_dict[node_id]
            ax.scatter(x, y, z, c=colors[brick], s=100, label=f'Brick {brick}')

    # 移除重複的圖例
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))

    # 設置視角和標題
    ax.view_init(elev=30, azim=45)
    ax.set_title('Pyramid Solution')
    
    # 設置軸標籤
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 顯示圖形
    plt.tight_layout()
    plt.show()

    # 保存圖片
    plt.savefig('solution_3d.png', bbox_inches='tight', dpi=300)

def main():
    # 載入解答
    with open('dlx_solution.pkl', 'rb') as f:
        solution = pickle.load(f)
    print(solution)
    
    # 轉換格式
    solution_list = [(brick, positions) for brick, positions in solution.items()]
    
    # 繪製解答
    plot_solution(solution_list)

if __name__ == '__main__':
    main()
