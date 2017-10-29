import numpy as np

class Circuit:
    """Essentially a Graph consisting of Vertices and Edges"""
    def __init__(self, V, E):
        self.__vertices = V
        self.__edges = E
        self.validate()

    def vertices():
        doc = "Vertices of the Circuit"
        def fget(self):
            return self.__vertices
        def fset(self, value):
            self.__vertices = value
        def fdel(self):
            del self.__vertices
        return locals()
    vertices = property(**vertices())

    def edges():
        doc = "The _edges property."
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
            A[self.edges[e, 0], self.edges[e, 1]] = 1

        return A

    def validate(self):
        """Check that a valid circuit has been made"""
