from components import *
from circuit import Circuit
from algorithms import subsetof
import numpy as np

num_comps = 0
while not (1 < num_comps < 21):
    num_comps = int(input("How many components will the circuit contain?\n>>"))

comps = []
comp_names = ["BATTERY", "JUNCTION", "RESISTOR", "BULB", "CAPACITOR"]
comp_data = {
    "BATTERY": {
        "lower_bound": 1e-03, #exclusive
        "upper_bound": 100., #inclusive
        "msg": "voltage.",
        "comp": DC_Battery
    },
    "JUNCTION": {
        "lower_bound": 2,
        "upper_bound": 5,
        "msg": "the number of connections.",
        "comp": Junction
    },
    "RESISTOR": {
        "lower_bound": 1e-03,
        "upper_bound": 1000.,
        "msg": "resistance.",
        "comp": Resistor
    },
    "CAPACITOR": {
        "lower_bound": 1e-03,
        "upper_bound": 100.,
        "msg": "capacitance (microfarads).",
        "comp": Capacitor
    }
}


for i in range(num_comps):
    comps.append(0)
    comps[i] = input("({0}) What kind of component?\n>>".format(i)).upper()
    while not comps[i] in comp_names:
        comps[i] = input("BATTERY | JUNCTION | RESISTOR | BULB | CAPACITOR\n>>").upper()

    if comps[i] == "BULB":
        r = 0
        while not (1e-03 < r <= 1000.):
            r = float(input('Please enter resistance.\n>>'))
        w = 0
        while not (1. < w <= 100.):
            w = float(input('Please enter wattage.\n>>'))
        comps[i] = Light_Bulb(r, w, i)
    else:
        elem = comp_data[comps[i]]
        inp = 0
        while not (elem["lower_bound"] < inp <= elem["upper_bound"]):
            inp = float(input("Please enter {0}\n>>".format(elem["msg"])))
        comps[i] = elem["comp"](i, inp)

wires = []

def show_components():
    print("==========")
    print("COMPONENTS")
    print("==========")

    for i in range(len(comps)):
        print(i, comps[i])


def show_wires():
    print("\n==========")
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
        if len((np.where(np.array([wires]) == i))[0]) < 2:
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
        return False

    if subsetof([[c1, c2]], wires):
        if len(comps) != 2:
            return False
        else:
            pass

    return not (c1 == c2 or comps[c1].is_fully_connected or comps[c2].is_fully_connected)


while not is_complete():

    c1, c2 = -2, -2 # just some initial states
    while not is_conn_valid(c1, c2):
        show_components()
        if len(wires) > 0:
            show_wires()
            
        c1 = int(input("Enter start point.\n>>"))
        c2 = int(input("Enter end point.\n>>"))

    comps[c1].add_connection(c2)
    comps[c2].add_connection(c1)
    wires.append([c1, c2])


# reformat wires
for i in range(len(wires)):
    wires[i] = Wire(wires[i][0], wires[i][1])



circ = Circuit(comps, wires)

print('done')
