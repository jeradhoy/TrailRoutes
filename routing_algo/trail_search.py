from typing import *
import psycopg2
#import database

def get_trails(conn, junct_id, max_dist):

    stmt = """
    SELECT t.id, t.length_mi, t.junct1, t.junct2
        FROM junctions as j, trail_junct_rel AS t
        WHERE j.junct_id = %s AND
        ST_DWithin(t.geom, j.geom, %s);
    """
    cur = conn.cursor()
    cur.execute(stmt, (junct_id, max_dist*1609.34))
    data = cur.fetchall()
    cur.close()
    return data


def get_all_loops(conn, junct_id, max_dist):
    
    trail_list = get_trails(conn, junct_id, max_dist)

    node_dict = create_node_dict(trail_list)

    loops = find_loops(node_dict, junct_id, 0, max_dist)

    return(loops)


# {trail_id: [(node_1, node_2, dist)]}
def create_node_dict(trail_list: List) -> Dict:
    node_dict = {}

    for trail in trail_list:
        start_node = trail[2]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append((trail[3], trail[0], trail[1]))

    for trail in trail_list:
        start_node = trail[3]
        if start_node not in node_dict:
            node_dict[start_node] = []
        node_dict[start_node].append((trail[2], trail[0], trail[1]))

    return node_dict



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
    path_list_tuple = [(tuple([path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None]), butt[2]) for butt in butts]
    # Thought I might be fixing a unique issue here, but idk if i did
    path_list_unique = list(set(path_list_tuple))
    path_list_dict = [{"trails": path[0] , "dist": path[1]} for path in path_list_unique]
    #path_list_dict = [{"trails": [path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None], "dist": butt[2]} for butt in butts]
    return sorted(path_list_dict, key = lambda entry: entry["dist"], reverse=True)


if __name__ == "__main__":
    node_dict = create_node_dict(trail_list)
    print(find_loops(node_dict, 5924, 5, 10))