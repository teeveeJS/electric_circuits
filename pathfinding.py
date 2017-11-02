import numpy as np
from algorithms import backtracker#, greedy

def get_neighbors(Graph, vertex):
    # why is this so ugly??? T_T
    neighbors = []
    for edge in Graph.edges:
        if edge[0] == vertex:
            neighbors.append(edge[1])
        elif edge[1] == vertex:
            neighbors.append(edge[0])
    return neighbors


def shortest_closed_loop(Graph, start_vertex):
    """
    Calculates the shortest closed loop of Graph with the given start_vertex
    * Note: take advantage of the fact that start_vertex must have exactly 2 cxns
    args:
        Graph: Class G(V, E) [Class Circuit for this project]
        start_vertex: a member of V
            * Note: members of V must have a cost property [R for this project]
            * Note: members of V must have a property that correlates each
            vertex to an endpoint of an edge [name for this project]
    returns:
        float. the cost of the shortest closed loop.
            * -1 if there are no closed loops
    """


    # recursive backtracker?
