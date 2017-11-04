import numpy as np
from components import *
from algorithms import backtracker, greedy, get_neighbor_edges

class Circuit:
    """
    Graph consisting of Vertices and Edges G(V, E)
    Vertices are Components and Edges are Wires
    """
    def __init__(self, V, E):
        self.__vertices = V
        self.__edges = E

        self.validate()

    def vertices():
        doc = "Vertices (components) of the Circuit: an array of Components"
        def fget(self):
            return self.__vertices
        def fset(self, value):
            self.__vertices = value
        def fdel(self):
            del self.__vertices
        return locals()
    vertices = property(**vertices())

    def edges():
        doc = "Edges (connections) of the Circuit: an array of Wires"
        def fget(self):
            return self.__edges
        def fset(self, value):
            self.__edges = value
        def fdel(self):
            del self.__edges
        return locals()
    edges = property(**edges())

    @property
    def edge_tuples(self):
        """Reformats the edges for ease-of-use with some algorithms"""
        return list(map(lambda e: e.pair, self.edges))

    @property
    def adjcy_matrix(self):
        A = np.zeros((len(self.vertices), len(self.vertices)))

        for e in self.edge_tuples:
            A[e[0], e[1]] = 1
            A[e[1], e[0]] = 1 # the connection goes both ways

        return A

    def validate(self):
        """
        Check that a valid circuit has been made.
        Criteria for a valid circuit:
        * at least one closed loop with:
            * non-zero resistance
                * greedy to check this
            * at least one source of emf
                * doesn't have be a battery: could be a capacitor or an inductor
        * recursive backtracking that there is a closed loop around the emf source
        * if there are components with less than 2 connections, immediately tell
        the user to complete the circuit

        How to accomplish this?
        1. Locate all emf sources (batteries, capacitors, inductors)
        2. For each, keep calculating loops until a closed loop with non-zero
        equivalent resistance is found
            * When found, break and return True
            * If not found, the circuit is not valid
        """
        for comp in self.vertices:
            # add isinstance(comp, Inductor)
            if isinstance(comp, DC_Battery) or isinstance(comp, Capacitor):
                if (not backtracker(self, comp.name) is None) and \
                   greedy(self, comp.name):
                        return True # circuit is valid

        return False # circuit is not valid

    def run(self):
        # this is where all the calculations will take place
        self.add_ground()


        return None

    def add_component(self, component):
        self.vertices = np.insert(self.vertices, len(self.vertices), component)
        return None

    def add_ground(self):
        # add a Ground to the circuit
        ground = Ground(len(self.vertices))
        self.add_component(ground)
        # the circuit needs to be broken open so that the Ground can be connected
        break_edge = None
        for comp in self.vertices:
            # simply place the Ground next to the first found emf source
            if isinstance(comp, DC_Battery) or isinstance(comp, Capacitor):
                break_edge = get_neighbor_edges(self, comp.name)[0]
                break
        # delete break_edge from self.edges
        # then form two new Wires to self.edges with Ground inserted in between
        for i in range(len(self.edges)):
            if np.array_equal(self.edges[i], break_edge):
                self.edges = np.delete(self.edges, i, 0)
                break

        print(self.edge_tuples)

        self.edges = np.insert(self.edges, len(self.edges), Wire(break_edge[0], ground.name), 0)
        self.edges = np.insert(self.edges, len(self.edges), Wire(break_edge[1], ground.name), 0)

        return None
