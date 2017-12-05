from components import *
from circuit import Circuit
from algorithms import subsetof
from sample_circuits import create_samples
import sys
import numpy as np


def valid_file_name(s):
    """Check if the input string follows the guidelines of a valid filename"""
    disallowed = ["\'", "\"", "~", "#", "%", "&", "*", "{", "}", "\\", ":", \
                  "<", ">", "?", "/", "|", ".", ",", ";"]
    if len(s) == 0 or len(s) > 50:
        return False
    # prohibit hidden files. also takes care of _vti_
    if s[0] == "_":
        return False
    for c in s:
        if c in disallowed:
            return False
    # bunch of other checks that i'll ignore
    return True


num_comps = 0
while not (1 <= num_comps < 21):
    print("Enter 1 to load Circuit from file")
    num_comps = int(input("How many components will the circuit contain?\n>>"))


# The user has chosen to load circuit data from an external file
if num_comps == 1:
    file_name = ""
    while not valid_file_name(file_name):
        file_name = input("Enter file name.\n>>").strip()
    
    create_samples(file_name)
    circ = Circuit(*np.load(file_name + ".npy"))

    print('done')
    sys.exit()


# The component and wire lists to be filled by the user
comps = []
wires = []
# All the components available to the user
comp_names = ["BATTERY", "JUNCTION", "RESISTOR", "BULB", "CAPACITOR", "MULTI_METER"]
# A nice way to keep track of the data to be collected and to reinforce bounds
comp_data = {
    "BATTERY": {
        "lower_bound": [1e-03],
        "upper_bound": [100.],
        "msg": ["voltage."],
        "comp": DC_Battery
    },
    "JUNCTION": {
        "lower_bound": [3],
        "upper_bound": [5],
        "msg": ["the number of connections."],
        "comp": Junction
    },
    "RESISTOR": {
        "lower_bound": [1e-03],
        "upper_bound": [1000.],
        "msg": ["resistance."],
        "comp": Resistor
    },
    "CAPACITOR": {
        "lower_bound": [1e-03, 0.],
        "upper_bound": [100., 100.],
        "msg": ["capacitance (microfarads).", "initial voltage."],
        "comp": Capacitor
    },
    "BULB": {
        "lower_bound": [1e-03, 1.],
        "upper_bound": [1000., 100.],
        "msg": ["resistance.", "wattage."],
        "comp": Light_Bulb
    }
}


# Gather all the data for the components
for i in range(num_comps):
    comps.append(0)
    comps[i] = input("({0}) What kind of component?\n>>".format(i)).upper()
    while not comps[i] in comp_names:
        comps[i] = input(" | ".join(comp_data.keys()) + " | MULTI_METER\n>>").upper()

    if comps[i] == "MULTI_METER":
        t = None
        while t != "VOLTMETER" or t != "AMMETER":
            t = input("Please enter meter type: VOLTMETER | AMMETER.\n>>").upper()
        if t == "AMMETER":
            comps[i] = Multimeter(Meter_Type.AMMETER)
        else:
            comps[i] = Multimeter()
    else:
        elem = comp_data[comps[i]]
        args = []
        for j in range(len(elem["lower_bound"])):
            inp = -1
            while not (elem["lower_bound"][j] <= inp <= elem["upper_bound"][j]):
                inp = float(input("Please enter {0}\n>>".format(elem["msg"][j])))
            args.append(inp)
        comps[i] = elem["comp"](*args)


def show_components():
    """Prints the components so that the user can easier create the connections"""
    print("==========")
    print("COMPONENTS")
    print("==========")

    for i in range(len(comps)):
        print(i, type(comps[i]))


def show_wires():
    """Prints the current wires the user has created"""
    print("\n==========")
    print("WIRES")
    print("==========")

    for i in range(len(wires)):
        print("({0}, {1})".format(wires[i][0], wires[i][1]))

    print('\n')


def is_complete():
    """checks completeness of the template-circuit based on wires"""
    # each component must have at least two connections

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

    if subsetof([[c1, c2]], wires): # Wire(c1, c2) in wires
        if len(comps) != 2:
            return False
        else:
            pass

    return not (c1 == c2 or comps[c1].is_fully_connected or comps[c2].is_fully_connected)


while not is_complete():
    """The circuit is not complete so the user must keep adding wires to the circuit"""
    c1, c2 = -2, -2 # just some initial states
    while not is_conn_valid(c1, c2):
        show_components()
        if len(wires) > 0:
            show_wires()

        c1 = int(input("Enter start point.\n>>"))
        c2 = int(input("Enter end point.\n>>"))

    comps[c1].add_connection(c2)
    comps[c2].add_connection(c1)
    wires.append([c1, c2]) # wires.append(Wire(c1, c2))


# Reformats wires
#TODO: get rid of this. i.e. directly append Wires
for i in range(len(wires)):
    wires[i] = Wire(wires[i][0], wires[i][1])


if input("Would you like to save the circuit?\n>>").strip() == "y":
    c_name = ""
    while not valid_file_name(c_name):
        c_name = input("Enter file name without extension\n>>").strip()
    np.save(c_name, np.array([comps, wires]))

# Creates the actual circuit and starts all the calculations
circ = Circuit(comps, wires)

print('done')
