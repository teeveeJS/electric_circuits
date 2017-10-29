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


class Wire(Component):
    def __init__(self, R=0):
        super().__init__(0, 0, R)

class Emf_Source(Component):
    def __init__(self, V=3, R=0):
        #R represents the battery's internal resistance
        super().__init__(V, 0, R)

class Resistor(Component):
    def __init__(self, R=5):
        super().__init__(0, 0, R)

class Capacitor(Component):
    """
    Parallel-plate capacitor
    A: area of the plate
    C: capacitance
    d: distance of separation between the plates
    V: voltage across the parallel plates
    Q: charge of the capacitor
    kappa: the dielectric constant (1 in vacuum)
    epsilon: permittivity of the dielectric = vacuum permittivity * kappa
    """
    def __init__(self, V, A, d, kappa=1):
        super().__init__(V, 0, 0)
        self.epsilon = kappa * 8.854e-12
        self.__C = self.epsilon * A / d
        self.__Q = self.cpty * self.emf

    def cpty():
        doc = "The Capacitance property."
        def fget(self):
            return self.__C
        def fset(self, value):
            self.__C = value
        def fdel(self):
            del self.__C
        return locals()
    cpty = property(**cpty())

    def chg():
        doc = "The Charge property."
        def fget(self):
            return self.__Q
        def fset(self, value):
            self.__Q = value
        def fdel(self):
            del self.__Q
        return locals()
    chg = property(**chg())


# example
# wire = Component(4, 3, 0.1)
# wire.emf
# wire.curr
# wire.res
# wire.emf = 5
# wire.curr = 2
# wire.res = 0
