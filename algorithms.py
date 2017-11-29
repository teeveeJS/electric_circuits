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
            if np.array_equal(i, j) or np.array_equal(i, j[::-1]):
                matches += 1
    return len(a) == matches


def backtracker(Graph, target, current_node, visited_nodes, available_edges):
    visited_nodes.append(current_node)


    print(visited_nodes, available_edges, [[target, current_node]])


    global total_res
    if subsetof([[target, current_node]], available_edges):
        print("found a loop")
        total_res += Graph.vertices[current_node].res
        return total_res

    if is_repeating(visited_nodes):
        # no loop found
        print("circuit is repeating: no loop")
        return -1

    if len(available_edges) == 0:
        print("all edges traversed: no loop found")
        return -1

    for e in available_edges:
        if e[0] == current_node:
            print('e2')
            total_res += Graph.vertices[current_node].res
            available_edges.pop(available_edges.index(e))
            return backtracker(Graph, target, e[1], visited_nodes, available_edges)
        elif e[1] == current_node:
            print('e1')
            total_res += Graph.vertices[current_node].res
            available_edges.pop(available_edges.index(e))
            return backtracker(Graph, target, e[0], visited_nodes, available_edges)

    print('backtracking')
    return backtracker(Graph, target, visited_nodes[-1], visited_nodes, available_edges)
