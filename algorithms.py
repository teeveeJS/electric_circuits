import numpy as np

# total resistance in a circuit. could be one of backtracker's params
total_res = 0


def is_repeating(hist):
    """
    Checks if list is repeating. A list is repeating if the same two elements
    occur repeatedly at the end.
    """
    l = len(hist)
    if l < 4:
        return False
    else:
        return hist[l-1] == hist[l-3] and hist[l-2] == hist[l-4]


def subsetof(a, b):
    """Checks if list a is a subset of list b"""
    matches = 0
    for i in a:
        for j in b:
            if np.array_equal(i, j) or np.array_equal(i, j[::-1]):
                matches += 1
    return len(a) == matches


def backtracker(Graph, target, current_node, visited_nodes, available_edges):
    """
    Backtracking algorithm to find a path from the first current_node to target
    params:
        Graph: G(V, E). structure of edges and vertices
        target: int. index representing the goal node
        current_node: int. index representing the node being considered
        visited_nodes: list of nodes that have been visited
        available_edges: list of edges that have not been traversed
    returns:
        float. the total resistance of traversing the found loop.
            -1 if no loop found
    """

    # print(visited_nodes, available_edges, [[target, current_node]])

    global total_res
    if subsetof([[target, current_node]], available_edges):
        # can traverse to the target node; a valid loop has been formed
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

    next_node = None
    least_res = np.inf
    # loop through all the available edges
    for e in available_edges:
        # TODO: prioritize the path of least resistance instead of just taking
        # available edge that connects to current_node.
        if current_node in e:
            opposite_e = e[~e.index(current_node)+2]
            if Graph.vertices[opposite_e].res < least_res:
                next_node = opposite_e
                least_res = Graph.vertices[opposite_e].res
                
                if least_res == 0:
                    # no need to keep looking further
                    break
        
    if next_node != None:
        visited_nodes.append(current_node)
        total_res += Graph.vertices[current_node].res
        available_edges.pop(available_edges.index(e))
        return backtracker(Graph, target, next_node, visited_nodes, available_edges)

    # No viable next node found; have to backtrack
    next_node = visited_nodes[-2]
    print("backtracking to", next_node)
    # Subtract the cost of the next node so that it is not double added
    total_res -= Graph.vertices[next_node].res
    # TODO: could return an array instead and compute cost from that
    return backtracker(Graph, target, next_node, visited_nodes, available_edges)
