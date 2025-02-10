import pickle

def read_puzzle_constraints():
    """
    讀取題目約束，格式為：Brick: [cell1, cell2, ...]
    使用者輸入空行表示結束輸入。
    回傳一個 dict，key 為 brick 名稱，value 為一個 set，表示必須包含的 cell。
    """
    print("請輸入題目約束（例如：B:[0, 1, 2, 3, 8]），每行一個，輸入空行結束：")
    constraints = {}
    while True:
        line = input().strip()
        if not line:
            break
        if ':' not in line:
            print("格式錯誤，請包含 ':' 字元。")
            continue
        brick, cells_str = line.split(':', 1)
        brick = brick.strip()
        cells_str = cells_str.strip()
        if cells_str.startswith('[') and cells_str.endswith(']'):
            cells_str = cells_str[1:-1]
        try:
            # 將每個 cell 轉換成 int
            cells = [int(x.strip()) for x in cells_str.split(',') if x.strip()]
        except Exception as e:
            print("解析數字失敗，請重新輸入。")
            continue
        constraints[brick] = set(cells)
    return constraints

def solve_bruteforce(brick_positions, num_cells):
    """
    利用回溯法暴力搜尋一組不重疊的 brick 放置方案，
    使得所有選定的放置方案覆蓋的 cell 總數等於 num_cells。
    
    brick_positions: dict，key 為 brick 名稱，value 為該 brick 的所有候選放置位置，
                     每個候選位置為一個 cell 數字列表。
    num_cells: 整個拼圖需要覆蓋的 cell 數目。
    
    回傳第一組找到的解答（dict 格式：{brick: 位置列表}），若無解則回傳 None。
    """
    # 將 brick 按照候選方案數量由少到多排序，這有助於剪枝
    bricks = sorted(brick_positions.keys(), key=lambda b: len(brick_positions[b]))
    
    solution_found = None  # 用來存放找到的解答

    def backtrack(index, used_cells, current_solution):
        nonlocal solution_found
        if solution_found is not None:
            return  # 已找到解答，提前返回
        
        # 當所有 brick 都處理完畢
        if index == len(bricks):
            if len(used_cells) == num_cells:
                solution_found = current_solution.copy()
            return
        
        brick = bricks[index]
        # 遍歷該 brick 的所有候選放置位置
        for pos in brick_positions[brick]:
            pos_set = set(pos)
            # 若此位置與已使用的 cell 有重疊則跳過
            if used_cells.intersection(pos_set):
                continue
            
            # 選擇此位置
            new_used = used_cells.union(pos_set)
            current_solution[brick] = pos
            
            backtrack(index + 1, new_used, current_solution)
            
            if solution_found is not None:
                return
            
            # 回溯：移除該 brick 的選擇
            del current_solution[brick]

    backtrack(0, set(), {})
    return solution_found

def main():
    print("Loading data...")
    # 從 pickle 檔案讀取 brick 可能放置的位置資料
    with open("brick_possible_pos.pkl", "rb") as f:
        brick_positions = pickle.load(f)
    
    # 讀取使用者輸入的題目約束
    constraints = read_puzzle_constraints()
    
    # 根據約束篩選 brick 的候選位置：
    # 若使用者對某 brick 設定了約束，則僅保留那些候選位置中包含約束所指定的 cell。
    for brick, required_cells in constraints.items():
        if brick in brick_positions:
            filtered = [pos for pos in brick_positions[brick] if required_cells.issubset(set(pos))]
            if not filtered:
                print(f"警告：Brick {brick} 沒有符合約束 {required_cells} 的候選位置！")
            brick_positions[brick] = filtered
        else:
            print(f"警告：Brick {brick} 不存在於候選位置資料中！")
    
    num_cells = 55  # 例如，金字塔（pyramid）的 cell 總數
    
    print("Solving puzzle using brute-force search...")
    solution = solve_bruteforce(brick_positions, num_cells)
    
    if solution:
        print("\n找到解答！")
        for brick, pos in solution.items():
            print(f"Brick {brick}: {pos}")
        # 將解答存到 pickle 檔案
        with open('brute_force_solution.pkl', 'wb') as f:
            pickle.dump(solution, f)
    else:
        print("\n找不到符合條件的解答。")

if __name__ == '__main__':
    main()
