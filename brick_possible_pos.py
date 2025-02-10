from collections import defaultdict
from brick_def import brick_fingerprint, brick_example
from pyrimid_def import pyrimid_def, neighbor_dict, position_dict
from pyrimid_def import yield_pyrimid
from utils import calc_distance
from itertools import combinations

from itertools import combinations
from collections import defaultdict
import multiprocessing as mp
from functools import partial
from tqdm import tqdm

def find_possible_nodes(current_node, target_size, target_fp, visited=None, depth=0):
    """Find all possible combinations of nodes starting from current_node"""
    if visited is None:
        visited = {current_node}
    
    if len(visited) == target_size:
        # Calculate fingerprint for complete set
        current_fp = []
        nodes_list = list(visited)
        for n1, n2 in combinations(nodes_list, 2):
            dist = round(calc_distance(n1, n2), 3)
            current_fp.append(dist)
            
        if sorted(current_fp) == target_fp:
            return [list(visited)]
        return []
    
    if depth > target_size:
        return []
    
    results = []
    neighbors = neighbor_dict[current_node[0]]
    
    candidates = []
    for n in neighbors:
        if position_dict[n] not in visited:
            candidates.append(position_dict[n])
    
    for r in range(1, min(len(candidates) + 1, target_size - len(visited) + 1)):
        for new_nodes in combinations(candidates, r):
            new_visited = visited | set(new_nodes)
            if len(new_visited) > target_size:
                continue
            
            # Continue exploring from each new node
            for new_node in new_nodes:
                more_results = find_possible_nodes(new_node, target_size, target_fp, new_visited, depth + 1)
                results.extend(more_results)
    
    return results

def process_node(args):
    """Process a single starting node - used by multiprocessing"""
    start_node, target_size, target_fp = args
    positions = find_possible_nodes(start_node, target_size, target_fp)
    return [(start_node[0], [n[0] for n in pos]) for pos in positions]

def main():
    all_nodes = list(yield_pyrimid())
    brick_avail_pos = defaultdict(list)
    
    num_cores = mp.cpu_count()
    pool = mp.Pool(processes=num_cores)
    print(f"Using {num_cores} CPU cores")

    for brick in brick_fingerprint:
        print(f"\nChecking Brick {brick}")
        target_size = len(brick_example[brick])
        target_fp = brick_fingerprint[brick]
        
        args_list = [(node, target_size, target_fp) for node in all_nodes]
        
        results = []
        for result in tqdm(pool.imap_unordered(process_node, args_list), 
                          total=len(args_list), 
                          desc=f"Processing Brick {brick}"):
            results.extend(result)
        
        # Collect unique results
        seen = set()
        for _, node_ids in results:
            node_ids_tuple = tuple(sorted(node_ids))
            if node_ids_tuple not in seen:
                seen.add(node_ids_tuple)
                brick_avail_pos[brick].append(list(node_ids_tuple))
                print(f"Found match at nodes: {list(node_ids_tuple)}")

    pool.close()
    pool.join()
    return brick_avail_pos

if __name__ == '__main__':
    result = main()
    for brick, positions in result.items():
        print(f"\nBrick {brick} can be placed in {len(positions)} ways:")
        for pos in positions:
            print(f"  Nodes: {pos}")

    print(result)
    for brick, positions in result.items():
        print(f"\nBrick {brick} can be placed in {len(positions)} ways")

    import pickle
    with open('brick_possible_pos.pkl', 'wb') as f:
        pickle.dump(result, f)
