import numpy as np

class Circuit:
    """Graph consisting of Vertices and Edges G(V, E)"""
    def __init__(self, V, E):
        self.__vertices = V
        self.__edges = E
        self.validate()

    def vertices():
        doc = "Vertices (components) of the Circuit"
        def fget(self):
            return self.__vertices
        def fset(self, value):
            self.__vertices = value
        def fdel(self):
            del self.__vertices
        return locals()
    vertices = property(**vertices())

    def edges():
        doc = "Edges (connections) of the circuit."
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
            * at least one source of emf
                * doesn't have be a battery: could be a capacitor or an inductor
        """

    def get_component(self, name):
        return self.vertices[name]

    def add_component(self, component):
        np.insert(self.vertices, len(self.vertices), component)
