from typing import *
import psycopg2
import copy
import time
import redis
import json
from collections import defaultdict

#import database

# Checks redis to see if path and milage already exist. 
# Returns None if trail has not been stored.
# Otherwise, returns the trails.
def get_redis(junct_id1,max_dist,junct_id2=""):

    r = redis.Redis(host='localhost', port=6379, db=0)

    redis_result = r.hget("trails",str(junct_id1)+
    ":"+str(junct_id2)+
    ":"+str(max_dist))
    
    if redis_result is None:
        return redis_result
    else: 
        return json.loads(redis_result)

# Stores the trails in redis under the keys.
def set_redis(junct_id1,max_dist,trails,junct_id2=""):
    
    r = redis.Redis(host='localhost', port=6379, db=0)

    r.hset("trails",str(junct_id1)+
    ":"+str(junct_id2)+
    ":"+str(max_dist),json.dumps(trails))
    

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
    
    # Check Redis first.
    redis_result = get_redis(junct_id,max_dist)
    if  not redis_result is None:
        return redis_result

    trail_list = get_trails(conn, junct_id, max_dist)

    node_dict = create_node_dict(trail_list)

    loops = find_loops(node_dict, junct_id, 0, max_dist)

    # Store redis results
    set_redis(junct_id,max_dist,loops)

    return(loops)

def get_point_to_point(conn, junct_id1, junct_id2, max_dist):
    
    # Check Redis first.
    redis_result = get_redis(junct_id1,max_dist,junct_id2)
    if  not redis_result is None:
        return redis_result

    trail_list = get_trails(conn, junct_id1, max_dist)

    node_dict = create_node_dict(trail_list)

    paths = find_all_paths(node_dict, junct_id1, max_dist, junct_id2)
    
    #paths = find_point_to_point(node_dict, junct_id1, junct_id2, 100)
    paths_processed = process_paths(paths)

    # Store redis results
    set_redis(junct_id1,max_dist,paths_processed,junct_id2)

    return paths_processed


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

    if current_node == target_node or current_node not in graph:
        return [path]

    if current_dist > max_dist:
        if target_node == None:
            return [path]
        else:
            return []


    for next_node in graph[current_node]:

        if next_node[0] not in [node[0] for node in path]:

            new_dist = current_dist + next_node[2]

            newpaths = find_all_paths(graph, next_node[0], max_dist, target_node, next_node[1], new_dist, path)

            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_all_paths2(graph, current_node, max_dist, target_node=None, trail_to=None, current_dist=0, path={}):


    if trail_to is not None:
        path = path + [(current_node, trail_to, current_dist)]

    paths = []

    # Only append each path if looking for loops...
    if target_node is None:
        paths.append(path)

    if current_node == target_node or current_node not in graph:
        return [path]

    if current_dist > max_dist:
        if target_node == None:
            return [path]
        else:
            return []


    for next_node in graph[current_node]:

        if next_node[0] not in [node[0] for node in path]:

            new_dist = current_dist + next_node[2]

            newpaths = find_all_paths(graph, next_node[0], max_dist, target_node, next_node[1], new_dist, path)

            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_p2p_dfs(conn, junct_id1, junct_id2, max_dist):

    trail_list1 = get_trails(conn, junct_id1, max_dist)
    node_dict1 = create_node_dict(trail_list1)

    trail_list2 = get_trails(conn, junct_id2, max_dist)
    node_dict2 = create_node_dict(trail_list2)

    paths1 = find_all_paths(node_dict1, junct_id1, max_dist/2)
    paths2 = find_all_paths(node_dict2, junct_id2, max_dist/2)

    butts = find_butted_paths(paths1, paths2, min_dist=0, max_dist=max_dist)

    print(butts)
    #print([tuple([paths1[butt[0]][0] + paths2[butt[1]][0][1:], butt[2]]) for butt in butts])



# So this finds dfs paths away from 

def find_butted_paths(path_list1, path_list2, min_dist, max_dist):

    path_ends1 = [(path[-1][0], path[-1][2]) for path in path_list1]
    path_ends2 = [(path[-1][0], path[-1][2]) for path in path_list2]

    loop_list = []
    for i, x in enumerate(path_ends1):
        for j, y in enumerate(path_ends2):
            if x[0] == y[0]:
                total_dist = x[1] + y[1]
                if total_dist < max_dist and total_dist > min_dist and (j, i, total_dist) not in loop_list:
                    loop_list.append((i, j, total_dist))
    return loop_list




def find_loops(graph, start_node, min_dist, max_dist):

    start = time.time()

    all_paths = find_all_paths(graph, start_node, max_dist/2)
    print(time.time() - start)
    butts = find_butted_paths(all_paths, all_paths, min_dist, max_dist)
    print(time.time() - start)
    path_list_tuple = [(tuple([path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None]), butt[2]) for butt in butts]
    # Thought I might be fixing a unique issue here, but idk if i did
    path_list_unique = list(set(path_list_tuple))
    path_list_dict = [{"trails": path[0] , "dist": path[1]} for path in path_list_unique]
    #path_list_dict = [{"trails": [path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None], "dist": butt[2]} for butt in butts]
    return sorted(path_list_dict, key = lambda entry: entry["dist"], reverse=True)


# Finds the point to point distance using a two way
def find_point_to_point(graph, start_point, end_point, max_paths):
    # TODO Max distance might be a good implementation idea to stop bfs from going out too far.
    # We can stop find the max bfs by looking at the distance between the start and end point.

    # Idea: Create a new path and path id for each neighbor.
    # Store a list of path ids with each vertex.
    # Will need a seperate visited list for each path.
    paths = set()

    front_queue = []
    front_queue.append([start_point])
    front_distances = []
    front_distances.append(0)

    back_queue = []
    back_queue.append([end_point])
    back_distances = []
    back_distances.append(0)

    # BFS
    # TODO: think about if I need to make this an or.
    while len(front_queue) > 0 and len(back_queue) > 0:

        # Front direction
        front_current_path = front_queue.pop(0)
        front_current_node = front_current_path[-1]
        front_current_distance = front_distances.pop(0)

        if (front_current_node == end_point):
            paths.add(tuple([tuple(front_current_path), front_current_distance]))
            if len(paths) == max_paths:
                return (list(paths))
            continue

        for i in range(0, len(back_queue)):
            if (back_queue[i][-1] == front_current_node):

                # TODO: Do visited bitvector implementation to speed things up.
                intersection = [value for value in front_current_path if value in back_queue[i]]
                if len(intersection) == 1:
                    back_queue[i].reverse()
                    new_path = front_current_path[:-1] + back_queue[i]
                    paths.add(tuple([tuple(new_path), back_distances[i] + front_current_distance]))
                    if len(paths) == max_paths:
                        return (list(paths))

                    break

        for neighbor in graph[front_current_node]:

            # TODO make visited array
            if not neighbor[0] in front_current_path:
                new_path = copy.deepcopy(front_current_path)
                new_path.append(neighbor[0])
                front_queue.append(new_path)
                front_distances.append(front_current_distance + neighbor[2])

        # Back direction
        back_current_path = back_queue.pop(0)
        back_current_node = back_current_path[-1]
        back_current_distance = back_distances.pop(0)

        if (back_current_node == start_point):
            back_current_path.reverse()
            paths.add(tuple([tuple(back_current_path), back_current_distance]))
            if len(paths) == max_paths:
                return (list(paths))
            continue

        for i in range(0, len(front_queue)):
            if front_queue[i][-1] == back_current_node:

                # TODO: Do visited bitvector implementation here to speed things up.
                intersection = [value for value in back_current_path if value in front_queue[i]]
                if len(intersection) == 1:
                    rev_back_path = copy.deepcopy(back_current_path)
                    rev_back_path.reverse()
                    new_path = front_queue[i] + rev_back_path[1:]
                    paths.add(tuple([tuple(new_path), back_current_distance + front_distances[i]]))
                    if len(paths) == max_paths:
                        return (list(paths))
                    break

        for neighbor in graph[back_current_node]:

            # TODO make visited array
            if not neighbor[0] in back_current_path:
                new_path = copy.deepcopy(back_current_path)
                new_path.append(neighbor[0])
                back_queue.append(new_path)
                back_distances.append(back_current_distance + neighbor[2])

    return (list(paths))

def process_paths(paths):

    path_list = [tuple([tuple([seg[1] for seg in path if seg[1] is not None]), path[-1][-1]]) for path in paths]
    path_list_unique = list(set(path_list))
    path_list_dict = [{"trails": path[0] , "dist": path[1]} for path in path_list_unique]
    #path_list_dict = [{"trails": [path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None], "dist": butt[2]} for butt in butts]
    return sorted(path_list_dict, key = lambda entry: entry["dist"], reverse=False)

if __name__ == "__main__":
    # set_redis(5924,34,[{"test":(1,2,3,4,6)}],99)
    # print(get_redis(5924,34,99))
    node_dict = create_node_dict(trail_list)
    print(find_loops(node_dict, 5924, 5, 10))