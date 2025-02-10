import pickle
from collections import defaultdict

def solve_pyramid_first(brick_positions):
    """
    Optimized solver to find the first valid solution quickly
    
    Optimizations:
    1. Sort bricks by number of possible positions (most constrained first)
    2. Early termination on first solution
    3. Forward checking to reduce search space
    """
    # Sort bricks by number of possible positions (ascending)
    bricks_sorted = sorted(brick_positions.keys(), 
                         key=lambda b: len(brick_positions[b]))
    
    # Track used positions and current solution
    used_positions = set()
    current_solution = {}
    
    def is_valid_remaining(remaining_bricks, available_positions):
        """Simple forward checking - ensure remaining bricks can still be placed"""
        return all(any(not pos_set.intersection(available_positions) 
                      for pos_set in brick_positions[brick])
                  for brick in remaining_bricks)
    
    def backtrack(brick_index):
        # Found a valid solution
        if brick_index == len(bricks_sorted):
            return True
            
        current_brick = bricks_sorted[brick_index]
        
        # Try each possible position for current brick
        for positions in brick_positions[current_brick]:
            positions_set = set(positions)
            
            # Check if position is available
            if not positions_set.intersection(used_positions):
                # Place the brick
                current_solution[current_brick] = positions
                used_positions.update(positions_set)
                
                # If found solution, propagate True back up
                if backtrack(brick_index + 1):
                    return True
                    
                # Remove the brick (backtrack)
                current_solution.pop(current_brick)
                used_positions.difference_update(positions_set)
        
        return False

    # Start backtracking with first brick
    found = backtrack(0)
    
    return current_solution if found else None

def main():
    # Load brick positions
    with open('brick_possible_pos.pkl', 'rb') as f:
        brick_positions = pickle.load(f)
    
    # Print initial statistics
    print("Number of possible positions per brick:")
    for brick in brick_positions:
        print(f"Brick {brick}: {len(brick_positions[brick])} positions")
    
    # Find first solution
    solution = solve_pyramid_first(brick_positions)
    
    if solution:
        print("\nFound a valid solution!")
        print("\nBrick placements:")
        for brick, positions in solution.items():
            print(f"Brick {brick}: {positions}")
        
        # Optionally save the solution
        with open('first_solution.pkl', 'wb') as f:
            pickle.dump(solution, f)
    else:
        print("\nNo solution found!")

if __name__ == '__main__':
    main()
