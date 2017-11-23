from components import *
from circuit import Circuit
from algorithms import subsetof
import numpy as np

num_comps = 0
while not (1 < num_comps < 21):
    num_comps = int(input("how many components will the circuit contain?"))

comps = []
comp_names = ["BATTERY", "JUNCTION", "RESISTOR", "BULB", "CAPACITOR"]


for i in range(num_comps):
    comps.append(0)
    comps[i] = input("what kind of component?").upper()
    while not comps[i] in comp_names:
        comps[i] = input("BATTERY | JUNCTION | RESISTOR | BULB | CAPACITOR").upper()


    # TODO: make this less stupid
    # sorry this is sooo ugly ;(
    if comps[i] == "BATTERY":
        v = 0
        while not (0 < v <= 100):
            v = int(input('please enter voltage'))
        comps[i] = DC_Battery(i, v)
    elif comps[i] == "JUNCTION":
        c = 0
        while not (2 < c <= 5):
            c = int(input('please enter the number of connections'))
        comps[i] = Junction(i, c)
    elif comps[i] == "RESISTOR":
        r = 0
        while not (0 < r <= 1000):
            r = int(input('please enter resistance'))
        comps[i] = Resistor(i, r)
    elif comps[i] == "BULB":
        r = 0
        while not (0 < r <= 1000):
            r = int(input('please enter resistance'))
        w = 0
        while not (0 < w <= 100):
            w = int(input('please enter wattage'))
        comps[i] = Light_Bulb(r, w, i)
    elif comps[i] == "CAPACITOR":
        c = 0.0
        while not (1e-10 < c <= 10.0):
            c = float(input('please enter capacitance'))
        comps[i] = Capacitor(i, c, 1)

wires = []

def show_components():
    print("==========")
    print("COMPONENTS")
    print("==========")

    for i in range(len(comps)):
        print(i, comps[i])

    print('\n')


def show_wires():
    print("==========")
    print("WIRES")
    print("==========")

    for i in range(len(wires)):
        print("({0}, {1})".format(wires[i][0], wires[i][1]))

    print('\n')


def is_complete():
    """checks completeness of the template-circuit based on wires"""
    # each component must have at least two connections
    # NOTE: the template-circuit doesn't contain Junctions at this point

    for i in range(len(comps)):
        if len((np.where(np.array([wires]) == i))[0]) != comps[i].len_conn:
            return False

    return True


def is_conn_valid(c1, c2):
    """
    checks if the user-defined connection is valid.

    1. component cannot be connected to itself
    2. equivalent connection should not exist already
        * NOTE: [c1, c2] and [c2, c1] are NOT equivalent
    3. the associated components should not be fully connected
    """

    # deal with the indices being out of bounds
    if not (0 <= c1 < len(comps) and 0 <= c2 < len(comps)):
        print('input values out of bounds')
        return False

    return not (c1 == c2 or subsetof([c1, c2], wires) or \
                comps[c1].is_fully_connected or comps[c2].is_fully_connected)


while True:
    break_signal = False

    c1, c2 = -2, -2 # just some initial states
    while not is_conn_valid(c1, c2):
        show_components()
        if len(wires) > 0:
            show_wires()
        print("enter -1 whenever you are done")
        c1 = int(input("enter start point"))
        c2 = int(input("enter end point"))

        if c1 == -1 or c2 == -1:
            break_signal = True
            break

    # TODO: some kind of automatic break: len(wires) = factorial(len(comps))
    # theoretical maximum

    if break_signal:
        if is_complete():
            print("You have finished building the circuit")
            break
        else:
            print("\nThe circuit is not yet complete!")
            break_signal = False

    comps[c1].add_connection(c2)
    comps[c2].add_connection(c1)
    wires.append([c1, c2])



# circ = Circuit(comps, wires)


print('done')
