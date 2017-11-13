import numpy as np

total_res = 0


def get_neighbors(Graph, vertex):
    neighbors = []
    for edge in Graph.edges:
        if edge.start == vertex:
            neighbors.append(edge.end)
        elif edge.end == vertex:
            neighbors.append(edge.start)
    return neighbors


def get_neighbor_edges(Graph, vertex):
    neighbors = []
    for edge in Graph.edge_tuples:
        if vertex in edge:
            neighbors.append(edge)
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
    # mark current node visited
    visited_nodes = np.append(visited_nodes, current_node)
    len_vis = len(visited_nodes)

    print(visited_nodes)

    # check if stuck in an infinite loop: no closed loop
    if is_repeating(visited_nodes):
        # no loop found
        print("circuit is repeating: no loop")
        return None

    vtxs = np.fromfunction(lambda i, j: j, (1, len(Graph.vertices)))
    if subsetof(vtxs, visited_nodes):
        # no loop found
        print("all edges traversed: no loop")
        return None

    global total_res
    current_res = np.inf
    current_next = None

    for n in get_neighbors(Graph, current_node):
        if not n in visited_nodes and Graph.vertices[n].res < current_res:
            current_res = Graph.vertices[n].res
            current_next = n

        elif (not subsetof([[current_node, n]], traversed_edges)) and \
            (not subsetof([[n, current_node]], traversed_edges)) and \
            (subsetof([[n, current_node]], Graph.edge_tuples) or \
            subsetof([[current_node, n]], Graph.edge_tuples)) and \
            np.array_equal(n, visited_nodes[0]):
                print("Found a loop!!!")
                return total_res#, visited_nodes

    if not current_next is None:
        total_res += current_res
        traversed_edges = np.append(traversed_edges, [[current_node, current_next]], axis=0)
        return backtracker(Graph, current_next, visited_nodes, traversed_edges)

    # has no unvisited nodes
    print('backtracking')
    return backtracker(Graph, visited_nodes[len_vis-2], visited_nodes, traversed_edges)


# def equipotentials(Graph, eqprs=np.array([]), start_edge=None):
#     """calculate all the equipotential regions in a circuit"""
#
#     if start_edge is None:
#         start_edge = Graph.edge_tuples[0]
#
#     current_region = np.array([])
#     current_edge = start_edge
#
#     while isinstance(Graph.vertices[current_edge[0]], Junction):
#         if not current_edge in eqprs:
#             current_region = np.append(current_region, current_edge)
#         # update current_edge
#
#
#
#     return eqprs
