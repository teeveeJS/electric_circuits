class Component:
    def __init__(self, V_o, I_o, R_o=0):
        self.__emf = V_o
        self.__I = I_o
        self.__R = R_o

    def emf():
        doc = "The emf property."
        def fget(self):
            return self.__emf
        def fset(self, value):
            self.__emf = value
        def fdel(self):
            del self.__emf
        return locals()
    emf = property(**emf())

    def curr():
        doc = "The current property."
        def fget(self):
            return self.__I
        def fset(self, value):
            self.__I = value
        def fdel(self):
            del self.__I
        return locals()
    curr = property(**curr())

    def res():
        doc = "The resistance property."
        def fget(self):
            return self.__R
        def fset(self, value):
            self.__R = value
        def fdel(self):
            del self.__R
        return locals()
    res = property(**res())

# example
# wire = Component(4, 3, 0.1)
# wire.emf
# wire.curr
# wire.res
# wire.emf = 5
# wire.curr = 2
# wire.res = 0
