import numpy as np
import pathfinding

class Circuit:
    """Graph consisting of Vertices and Edges G(V, E)"""
    def __init__(self, V, E):
        self.__vertices = V
        self.__edges = E
        self.validate()

    def vertices():
        doc = "Vertices (components) of the Circuit: an array of components"
        def fget(self):
            return self.__vertices
        def fset(self, value):
            self.__vertices = value
        def fdel(self):
            del self.__vertices
        return locals()
    vertices = property(**vertices())

    def edges():
        doc = "Edges (connections) of the circuit: an array of 2-tuples"
        def fget(self):
            return self.__edges
        def fset(self, value):
            self.__edges = value
        def fdel(self):
            del self.__edges
        return locals()
    edges = property(**edges())

    @property
    def adjcy_matrix(self):
        A = np.zeros((len(self.vertices), len(self.vertices)))

        for e in self.edges:
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
                if pathfinding.shortest_closed_loop(self, comp) > 0:
                    return True # valid

        return False # not valid



    def add_component(self, component):
        np.insert(self.vertices, len(self.vertices), component)
