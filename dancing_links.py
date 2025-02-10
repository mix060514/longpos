import sys
# Increase the recursion limit (if necessary)
sys.setrecursionlimit(10000)

class DLXNode:
    """
    Node for the doubly-linked structure.
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
    Column header node that holds the size (number of nodes in the column)
    and an optional name.
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
        
        # Create the column headers and link them in a circular doubly-linked list.
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
        """Add a row to the DLX structure given the list of column indices and a row_id."""
        first_node = None
        prev_node = None

        for c in cols:
            col_header = self.columns[c]
            node = DLXNode()
            node.column = col_header
            node.row_id = row_id

            # Insert node into the column (vertical linkage)
            node.down = col_header
            node.up = col_header.up
            col_header.up.down = node
            col_header.up = node
            col_header.size += 1

            # Link the node horizontally into the current row.
            if first_node is None:
                first_node = node
                # For a single node row, left/right point to itself.
                node.left = node
                node.right = node
            else:
                node.left = prev_node
                node.right = first_node
                prev_node.right = node
                first_node.left = node
            prev_node = node

    def cover(self, col):
        """Covers a column and removes all rows that use that column."""
        # Remove the column header from the list.
        col.right.left = col.left
        col.left.right = col.right
        
        i = col.down
        while i != col:
            j = i.right
            while j != i:
                # Remove node j from its column.
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col):
        """Reverses the cover operation (adds the column back)."""
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def choose_column(self):
        """
        Choose the column with the smallest size by iterating through the active
        columns (using the circular linked list starting at self.root.right).
        """
        best = None
        best_size = float('inf')
        col = self.root.right
        while col != self.root:
            if col.size < best_size:
                best_size = col.size
                best = col
                # Early exit if you find a column with size 1.
                if best_size == 1:
                    break
            col = col.right
        return best

    def search(self, solution, max_solutions=1, solutions=None):
        """
        Recursive DLX search for exact covers. When a complete solution is found,
        it is added (a copy of the current solution) to solutions.
        """
        if solutions is None:
            solutions = []
        if self.root.right == self.root:
            solutions.append(solution.copy())
            return solutions

        col = self.choose_column()
        if col is None or col.size == 0:
            # No valid column found – dead end.
            return solutions

        self.cover(col)
        row = col.down
        while row != col:
            solution.append(row)  # Choose this row.
            j = row.right
            while j != row:
                self.cover(j.column)
                j = j.right

            self.search(solution, max_solutions, solutions)
            if len(solutions) >= max_solutions:
                return solutions

            # Backtrack: remove the row and uncover columns.
            solution.pop()
            j = row.left
            while j != row:
                self.uncover(j.column)
                j = j.left
            row = row.down

        self.uncover(col)
        return solutions

def build_exact_cover_matrix(brick_positions, num_cells, brick_list):
    """
    Build the exact cover matrix. There are num_cells position constraints and an
    additional constraint for each brick.
    """
    total_cols = num_cells + len(brick_list)
    dlx = DLX(total_cols)
    
    brick_index = {brick: i for i, brick in enumerate(brick_list)}
    row_to_info = []  # Map row_id to (brick, pos_list)
    
    for brick in brick_list:
        b_idx = brick_index[brick]
        for pos_list in brick_positions[brick]:
            # The first column for this row corresponds to the brick constraint.
            row_cols = [num_cells + b_idx]
            # Then add the positions constraints.
            row_cols.extend(pos_list)
            row_cols = sorted(set(row_cols))
            
            row_id = len(row_to_info)
            dlx.add_row(row_cols, row_id)
            row_to_info.append((brick, pos_list))
    
    return dlx, row_to_info

def solve_with_dlx(brick_positions, num_cells):
    """
    Solve the puzzle using DLX and return a list of tuples (brick, positions)
    corresponding to the solution.
    """
    bricks = sorted(list(brick_positions.keys()))
    dlx, row_map = build_exact_cover_matrix(brick_positions, num_cells, bricks)
    
    # Find the first solution.
    solutions = dlx.search(solution=[], max_solutions=1)
    if not solutions:
        return []
        
    # Convert the solution rows back to brick placements.
    result = []
    first_solution = solutions[0]
    for row_node in first_solution:
        brick, positions = row_map[row_node.row_id]
        result.append((brick, positions))
    return result

def main():
    import pickle
    from tqdm import tqdm  # Optional: shows progress bars if needed.
    
    print("Loading data...")
    # Load the brick positions data from a pickle file.
    with open("brick_possible_pos.pkl", "rb") as f:
        brick_positions = pickle.load(f)
    
    num_cells = 55  # For example, number of pyramid cells.
    
    print("Solving puzzle...")
    # Solve the puzzle using DLX.
    solution = solve_with_dlx(brick_positions, num_cells)
    
    # Output the result.
    if solution:
        print("\nFound a solution!")
        ans_dict = {}
        for brick, positions in solution:
            print(f"Brick {brick}: {positions}")
            ans_dict[brick] = positions
        
        import pickle
        with open('dlx_solution.pkl', 'wb') as f:
            pickle.dump(ans_dict, f)
    else:
        print("\nNo solution found.")

if __name__ == "__main__":
    main()
