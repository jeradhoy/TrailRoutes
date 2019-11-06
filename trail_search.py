


from typing import *

#[ startNode, endNode, dist]
edge_list = [
    [0, 1, 1.5],
    [1, 2, 2],
    [1, 2, 3],
    [2, 3, 2.5]
]
edge_dict = {
    0: [(1, 1.5)],
    1: [(2, 2), (2, 3), (0, 1.5)],
    2: [(3, 2.5), (1, 2), (1, 3)]
}

paths = []

depth_limit = 10

#edge_dict: Dict[List[Tuple]], 
def find_loops(path: list, current_edge: Tuple, start_node: int, dist, depth):

    dist += current_edge[1]
    path += current_edge
    depth += 1

    # Base case
    if current_edge[0] == start_node or depth == depth_limit:
        return (path, dist)

    # Recursive case
    next_edge = edge_dict[current_edge[0]]

    for edge in next_edge:
        find_loops(path, edge, start_node, dist)

start_node_id = 0
find_loops([], (0, 1), 0, 0)