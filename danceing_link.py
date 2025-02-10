class DLXNode:
    """
    雙向十字鏈表的節點結構
    """
    __slots__ = ("left", "right", "up", "down", "column", "row_id")

    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = None
        self.row_id = None

class ColumnHeader(DLXNode):
    """
    列頭節點，包含該列的大小信息
    """
    __slots__ = ("size", "name")

    def __init__(self, name=None):
        super().__init__()
        self.size = 0
        self.name = name

class DLX:
    def __init__(self, num_cols):
        self.root = ColumnHeader("root")
        self.columns = []
        
        # 建立列頭
        prev = self.root
        for c in range(num_cols):
            col = ColumnHeader(str(c))
            col.left = prev
            col.right = self.root
            prev.right = col
            self.root.left = col
            self.columns.append(col)
            prev = col

    def add_row(self, cols, row_id):
        """添加一行，並設置 row_id"""
        first_node = None
        prev_node = None

        for c in cols:
            col_header = self.columns[c]
            node = DLXNode()
            node.column = col_header
            node.row_id = row_id

            # 垂直連接
            node.down = col_header
            node.up = col_header.up
            col_header.up.down = node
            col_header.up = node
            col_header.size += 1

            # 水平連接
            if first_node is None:
                first_node = node
            node.left = prev_node if prev_node else node
            node.right = first_node if prev_node else node
            if prev_node:
                prev_node.right = node
            prev_node = node

    def cover(self, col):
        """覆蓋一列"""
        col.right.left = col.left
        col.left.right = col.right
        
        row = col.down
        while row != col:
            right = row.right
            while right != row:
                right.down.up = right.up
                right.up.down = right.down
                right.column.size -= 1
                right = right.right
            row = row.down

    def uncover(self, col):
        """取消覆蓋一列"""
        row = col.up
        while row != col:
            left = row.left
            while left != row:
                left.column.size += 1
                left.down.up = left
                left.up.down = left
                left = left.left
            row = row.up
        col.right.left = col
        col.left.right = col

    def search(self):
        """搜索解"""
        if self.root.right == self.root:
            yield []
            return

        # 選擇最小列
        col = min(
            (col for col in self.columns if col.size > 0),
            key=lambda col: col.size
        )

        self.cover(col)
        
        row = col.down
        while row != col:
            solution = [row]
            
            right = row.right
            while right != row:
                self.cover(right.column)
                right = right.right

            yield from ([r for r in solution + s] for s in self.search())

            left = row.left
            while left != row:
                self.uncover(left.column)
                left = left.left

            row = row.down
            
        self.uncover(col)

def build_exact_cover_matrix(brick_positions, num_cells, brick_list):
    """建立精確覆蓋矩陣"""
    total_cols = num_cells + len(brick_list)
    dlx = DLX(total_cols)
    
    brick_index = {b: i for i, b in enumerate(brick_list)}
    row_to_info = []
    
    for brick in brick_list:
        b_idx = brick_index[brick]
        for pos_list in brick_positions[brick]:
            row_cols = [num_cells + b_idx]  # 積木約束
            row_cols.extend(p for p in pos_list)  # 位置約束
            row_cols = sorted(set(row_cols))
            
            row_id = len(row_to_info)
            dlx.add_row(row_cols, row_id)
            row_to_info.append((brick, pos_list))
    
    return dlx, row_to_info

def solve_with_dlx(brick_positions, num_cells):
    """使用 DLX 求解拼圖"""
    bricks = sorted(list(brick_positions.keys()))
    dlx, row_map = build_exact_cover_matrix(brick_positions, num_cells, bricks)
    
    # 尋找第一個解
    for solution_rows in dlx.search():
        result = []
        for row_node in solution_rows:
            brick, positions = row_map[row_node.row_id]
            result.append((brick, positions))
        return result  # 只返回第一個解
    
    return []  # 沒有找到解

def main():
    import pickle
    
    # 載入數據
    with open("brick_possible_pos.pkl", "rb") as f:
        brick_positions = pickle.load(f)
    
    num_cells = 55  # 金字塔格子數
    
    # 求解
    solution = solve_with_dlx(brick_positions, num_cells)
    
    # 輸出結果
    if solution:
        print("Found a solution!")
        for brick, positions in solution:
            print(f"Brick {brick}: {positions}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
