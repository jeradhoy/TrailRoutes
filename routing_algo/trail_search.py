


from typing import *

# trail_num, junct1, Node2, dist

trail_list = [
    ["1", "a", "b", 1],
    ["2", "b", "c", 1.5],
    ["3", "b", "c", 2],
    ["4", "c", "d", 2]
]

def create_trail_dict(trail_list: List) -> Dict:
    trail_dict = {}
    for trail in trail_list:
        trail_dict[trail[0]] = {"junct1": trail[1], "junct2": trail[2], "dist": trail[3]}
    return trail_dict

def create_node_dict(trail_list: List) -> Dict:
    node_dict = {}

    for trail in trail_list:
        start_node = trail[1]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append({"trail": trail[0], "end": trail[2], "dist": trail[3]})

    for trail in trail_list:
        start_node = trail[2]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append({"trail": trail[0], "end": trail[1], "dist": trail[3]})
    return node_dict

def create_node_dict(trail_list: List) -> Dict:
    node_dict = {}

    for trail in trail_list:
        start_node = trail[1]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append((trail[2], trail[0], trail[3]))

    for trail in trail_list:
        start_node = trail[2]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append((trail[1], trail[0], trail[3]))

    return node_dict



def create_node_dict2(trail_list: List) -> Dict:
    node_dict = {}

    for trail in trail_list:
        start_node = trail[1]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append((trail[2], trail[3]))

    for trail in trail_list:
        start_node = trail[2]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append((trail[1], trail[3]))
    return node_dict


trail_dict = create_trail_dict(trail_list)
node_dict = create_node_dict(trail_list)
node_dict2 = create_node_dict2(trail_list)

my_graph = {
    "a": [("b", "1", 1)],
    "b": [("c", "2", 1.5), ("c", "3", 2)],
    "c": [("d", "4", 3)],
    "d": [("e", "5", 2), ("f", "6", 3)],
    "f": [("g", "7", 3)]

}

def find_all_paths(graph, current_node, max_dist, target_node=None, trail_to=None, current_dist=0, path=[]):


    path = path + [(current_node, trail_to, current_dist)]
    paths = []

    # Only append each path if looking for loops...
    if target_node is None:
        paths.append(path)

    if current_dist > max_dist or current_node not in graph or current_node == target_node:
        return [path]


    for next_node in graph[current_node]:

        if next_node[0] not in [node[0] for node in path]:

            new_dist = current_dist + next_node[2]

            newpaths = find_all_paths(graph, next_node[0], max_dist, target_node, next_node[1], new_dist, path)

            for newpath in newpaths:
                paths.append(newpath)
    return paths


# So this finds dfs paths away from 

def find_butted_paths(path_list, min_dist, max_dist):
    path_ends = [(path[-1][0], path[-1][2]) for path in path_list]
    loop_list = []
    for i, x in enumerate(path_ends):
        for j, y in enumerate(path_ends):
            if x[0] == y[0]:
                total_dist = x[1] + y[1]
                if total_dist < max_dist and total_dist > min_dist and (j, i, total_dist) not in loop_list:
                    loop_list.append((i, j, total_dist))
    return loop_list



def find_loops(graph, start_node, min_dist, max_dist):

    all_paths = find_all_paths(graph, start_node, max_dist/2)
    butts = find_butted_paths(all_paths, min_dist, max_dist)
    return [([path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None], butt[2]) for butt in butts]

find_loops(node_dict, "a", 5, 10)