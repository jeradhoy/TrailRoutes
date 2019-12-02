def get_all_loops(conn,junct_id,distance):
    conn = psycopg2.connect(dbname="trailDb", user="postgres", host="localhost", password="meow")
    
    trail_list = get_trails(conn,junct_id,distance)

    node_dict = create_node_dict(trail_list)
    loops = find_loops(node_dict, 5924, 5, 10)

    conn.close()

    return(loops)


# {trail_id: [(node_1, node_2, dist)]}
def create_node_dict(trail_list):
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
    return [([path[1] for path in all_paths[butt[0]] if path[1] is not None] + [path[1] for path in all_paths[butt[1]][::-1] if path[1] is not None], butt[2]) for butt in butts]


# {trail_id: [(node_1, node_2, dist)]}
# graph = {node_id,[(node_id,pathlabel,dist)]}
def find_point_to_point(graph,start_point,end_point,max_paths):
    # TODO Max distance might be a good implementation idea to stop bfs from going out too far.
    # We can stop find the max bfs by looking at the distance between the start and end point.
    
    # Idea: Create a new path and path id for each neighbor. Make sure to prune and delete old paths.
    # Store a list of path ids with each vertex. 
    # Will need a seperate visited list for each path.
    paths={}

    node_queue = []
    node_queue.append(start_point)

    path_ids = {}
    visited={}
    for node_id in graph:
        path_ids[node_id]=[]
        visited[node_id]=False
    visited[start_point]=True
    path_ids[start_point].append(0)
    paths[0]=[start_point]

    while node_queue:
        
        current_node=node_queue.pop(0)
        print(current_node)

        for neighbor in graph[current_node]: 
            neighbor = neighbor[0]
            # TODO update distance here.
            if visited[neighbor] == False: 
                node_queue.append(neighbor) 
                visited[neighbor] = True

        



if __name__ == "__main__":
    sample_graph = [("a",1, 1,3),
                    ("b",1, 1,2),
                    ("c",1, 3,4),
                    ("d",1, 2,5),
                    ("e",1, 2,4),
                    ("f",1, 4,6),
                    ("g",1, 5,6),
                    ("h",1, 7,8)]
    node_dict = create_node_dict(sample_graph)
    find_loops(node_dict, 1, 0, 4)
    find_point_to_point(node_dict,1,6,7)