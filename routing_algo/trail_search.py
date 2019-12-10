from typing import *
import psycopg2
import copy
import time
import redis
import json
from collections import defaultdict

# Checks redis to see if path and milage already exist. 
# Returns None if trail has not been stored.
# Otherwise, returns the trails.
def check_redis(junct_id1,max_dist,junct_id2=""):

    r = redis.Redis(host='localhost', port=6379, db=0)

    preivous_max_dist = r.get(str(junct_id1) + ":" + str(junct_id2) + "_maxDist")

    if preivous_max_dist is None:
        return None

    preivous_max_dist = int(preivous_max_dist)

    if max_dist > preivous_max_dist:
        return None

    redis_result = json.loads(r.hget("trails", str(junct_id1) + ":" + str(junct_id2)))

    if max_dist < preivous_max_dist:
        redis_result = [trail for trail in redis_result if trail["dist"] <= max_dist]

    return redis_result

# Stores the trails in redis under the keys.
def set_redis(junct_id1,max_dist,trails,junct_id2=""):
    
    r = redis.Redis(host='localhost', port=6379, db=0)

    r.set(str(junct_id1) + ":" + str(junct_id2) + "_maxDist", max_dist)

    r.hset("trails",str(junct_id1)+
    ":"+str(junct_id2) ,json.dumps(trails))
    

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
    redis_result = check_redis(junct_id, max_dist)

    if redis_result is not None:
        print("Found redis cache, returning...")
        return redis_result

    trail_list = get_trails(conn, junct_id, max_dist)

    node_dict = create_node_dict(trail_list)

    loops = find_loops(node_dict, junct_id, 0, max_dist)

    #print(find_all_paths_dict(node_dict, junct_id, max_dist))

    # Store redis results
    set_redis(junct_id,max_dist,loops)

    return(loops)

def get_point_to_point(conn, junct_id1, junct_id2, max_dist):
    
    # Check Redis first.
    redis_result = check_redis(junct_id1, max_dist, junct_id2)
    if  not redis_result is None:
        print("Found redis cache, returning...")
        return redis_result

    print("Couldn't find redis cache, running DFS..")

    #paths_processed = find_p2p_dfs(conn, junct_id1, junct_id2, max_dist)

    trail_list = get_trails(conn, junct_id1, max_dist)

    node_dict = create_node_dict(trail_list)

    paths = find_all_paths(node_dict, junct_id1, max_dist, junct_id2)
    
    paths_processed = process_paths(paths)

    # Store redis results
    set_redis(junct_id1, max_dist, paths_processed, junct_id2)

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

# Rewriting to use dictionary so that butt end matching is much faster
def find_all_paths_dict(graph, current_node, max_dist, trail_to=None, current_dist=0, path=[]):

    if trail_to is not None:
        path = path + [(current_node, trail_to, current_dist)]

    paths = {}

    if current_dist > max_dist or current_node not in graph:
        return {current_node: [path]}


    for next_node in graph[current_node]:

        if next_node[0] not in [node[0] for node in path]:

            new_dist = current_dist + next_node[2]

            newpaths = find_all_paths_dict(graph, next_node[0], max_dist, next_node[1], new_dist, path)

            for butt, path_list in newpaths.items():
                paths.setdefault(butt, []).append(path_list)
    return paths

def find_p2p_dfs(conn, junct_id1, junct_id2, max_dist):

    trail_list1 = get_trails(conn, junct_id1, max_dist)
    node_dict1 = create_node_dict(trail_list1)

    trail_list2 = get_trails(conn, junct_id2, max_dist)
    node_dict2 = create_node_dict(trail_list2)

    paths1 = find_all_paths(node_dict1, junct_id1, max_dist/2)
    paths2 = find_all_paths(node_dict2, junct_id2, max_dist/2)

    butts = find_butted_paths(paths1, paths2, min_dist=0, max_dist=max_dist)


    path_list_tuple = [(tuple([path[1] for path in paths1[butt[0]] if path[1] is not None] + [path[1] for path in paths2[butt[1]][::-1] if path[1] is not None]), butt[2]) for butt in butts]

    path_list_unique = list(set(path_list_tuple))
    path_list_dict = [{"trails": path[0] , "dist": path[1]} for path in path_list_unique]

    return sorted(path_list_dict, key = lambda entry: entry["dist"], reverse=False)



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

    print("Time to find paths: " + str(time.time() - start))
    start = time.time()

    butts = find_butted_paths(all_paths, all_paths, min_dist, max_dist)

    print("Time to find butts :)" + str(time.time() - start))

    path_list_tuple = [(tuple([path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None]), butt[2]) for butt in butts]

    # Thought I might be fixing a unique issue here, but idk if i did
    path_list_unique = list(set(path_list_tuple))
    path_list_dict = [{"trails": path[0] , "dist": path[1]} for path in path_list_unique]

    return sorted(path_list_dict, key = lambda entry: entry["dist"], reverse=True)

def process_paths(paths):

    path_list = [tuple([tuple([seg[1] for seg in path if seg[1] is not None]), path[-1][-1]]) for path in paths]
    path_list_unique = list(set(path_list))
    path_list_dict = [{"trails": path[0] , "dist": path[1]} for path in path_list_unique]

    return sorted(path_list_dict, key = lambda entry: entry["dist"], reverse=False)

if __name__ == "__main__":
    conn = psycopg2.connect(dbname="trailDb", user="postgres", host="localhost", password="meow")
    node_dict = create_node_dict(get_trails(conn,5924,25))
    print(get_point_to_point(conn, 5891, 5924, 19))
    
    conn.close()