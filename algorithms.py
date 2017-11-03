import numpy as np

def get_neighbors(Graph, vertex):
    neighbors = []
    for edge in Graph.edges:
        if edge[0] == vertex:
            neighbors.append(edge[1])
        elif edge[1] == vertex:
            neighbors.append(edge[0])
    return neighbors

def is_repeating(hist):
    l = len(hist)
    if l < 4:
        return False
    else:
        return hist[l-1] == hist[l-3] and hist[l-2] == hist[l-4]


def subsetof(a, b):
    matches = 0
    for i in a:
        for j in b:
            if np.array_equal(i, j):
                matches += 1
    return len(a) == matches

def backtracker(Graph, current_node, visited_nodes=np.array([]), traversed_edges=np.array([[None, None]])):

    #print("current node:", current_node, visited_nodes)

    # mark current node visited
    visited_nodes = np.append(visited_nodes, current_node)
    len_vis = len(visited_nodes)


    # check if stuck in an infinite loop: no closed loop
    if is_repeating(visited_nodes):
        # no loop found
        return None

    vertices = np.fromfunction(lambda i, j: j, (1, len(Graph.vertices)))
    if subsetof(vertices, visited_nodes):
        # no loop found
        return None

    for n in get_neighbors(Graph, current_node):
        if not n in visited_nodes:
            # simply picks the first unvisited node
            traversed_edges = np.append(traversed_edges, [[current_node, n]], axis=0)
            return backtracker(Graph, n, visited_nodes, traversed_edges)
        elif (not subsetof([[current_node, n]], traversed_edges)) and \
            (not subsetof([[n, current_node]], traversed_edges)) and \
            (subsetof([[n, current_node]], Graph.edges) or \
            subsetof([[current_node, n]], Graph.edges)) and \
            np.array_equal(n, visited_nodes[0]):
                """Found a loop!!!"""
                return visited_nodes

    # has no unvisited nodes
    # print("backtracking to:", visited_nodes[len_vis-2])
    return backtracker(Graph, visited_nodes[len_vis-2], visited_nodes, traversed_edges)

def greedy(Graph, start_node, visited_nodes):
    """
    Greedy algorithm to check if Graph can be traversed
    with zero cost (resistance)
    """

    visited_nodes = np.append(visited_nodes, start_node)

    cost = np.inf
    current_next = None

    for n in get_neighbors(Graph, start_node):
        if not n in visited_nodes and Graph.vertices[n].res < cost:
            cost = Graph.vertices[n].res
            current_next = n

    if current_next != None:
        return greedy(Graph, current_next, visited_nodes)
