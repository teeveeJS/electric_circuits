import numpy as np
from components import *


def create_samples(data_key):

    data = {
        # a very simple circuit
        "c1": np.array([
            [
                DC_Battery(12),
                Resistor(5)
            ],
            [
                Wire(0, 1),
                Wire(1, 0)
            ]
        ]),
        # a more complex circuit
        "c2": np.array([
            [
                DC_Battery(100),
                Junction(),
                Junction(),
                Resistor(50),
                Resistor(40),
                Resistor(20),
                Junction(),
                Junction()
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(2, 4),
                Wire(2, 5),
                Wire(4, 6),
                Wire(5, 6),
                Wire(6, 7),
                Wire(1, 3),
                Wire(3, 7),
                Wire(0, 7)
            ]
        ]),
        # basic RC circuit
        "c3": np.array([
            [
                Capacitor(100, v_init=12),
                Resistor(1000)
            ],
            [
                Wire(0, 1),
                Wire(1, 0)
            ]
        ]),
        # charging a capacitor
        "c4": np.array([
            [
                Capacitor(100),
                Resistor(1000),
                DC_Battery(12)
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(2, 0)
            ]
        ]),

        # Circuit failures
        # two disjoint circuit
#        "c5": np.array([
#            [
#                DC_Battery(12),
#                Resistor(5),
#                DC_Battery(12),
#                Resistor(5)
#            ],
#            [
#                Wire(0, 1),
#                Wire(1, 0),
#                Wire(2, 3),
#                Wire(3, 2)
#            ]
#        ]),
        # invalid loop within a circuit
        # surprisingly, the computations come out correct
        "c6": np.array([
            [
                DC_Battery(12),
                Resistor(5),
                Junction(),
                Junction(),
                Resistor(3),
                Resistor(4)
            ],
            [
                Wire(0, 1),
                Wire(0, 2),
                Wire(1, 2),
                Wire(2, 3),
                Wire(3, 4),
                Wire(3, 5),
                Wire(4, 5)
            ]
        ]),

        #Other tests
        # two batteries with opposing ends
        "c7": np.array([
            [
                DC_Battery(12),
                DC_Battery(9),
                Resistor(50)
            ],
            [
                Wire(1, 0),
                Wire(1, 2),
                Wire(0, 2)
            ]
        ]),

        # time constant/numerical integration failures
        "c8": np.array([
            [
                DC_Battery(100),
                Resistor(500),
                Capacitor(1)
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(2, 0)
            ]
        ]),
        "c9": np.array([
            [
                DC_Battery(100),
                Resistor(5),
                Capacitor(1000)
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(2, 0)
            ]
        ]),

        # two capacitors
        "c10": np.array([
            [
                Capacitor(100, v_init=3),
                Capacitor(200, v_init=12),
                Resistor(2000)
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(0, 2)
            ]
        ]),

        # Voltmeter
        "c11": np.array([
            [
                DC_Battery(12),
                Multimeter(),
                Resistor(5),
                Junction(),
                Junction()
            ],
            [
                Wire(0, 3),
                Wire(3, 1),
                Wire(3, 2),
                Wire(2, 4),
                Wire(1, 4),
                Wire(4, 0)
            ]
        ]),

        # Ammeter
        "c12": np.array([
            [
                DC_Battery(12),
                Multimeter(Meter_Type.AMMETER),
                Resistor(5)
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(2, 0)
            ]
        ]),

        # wheatstone bridge
        "c13": np.array([
            [
                DC_Battery(100),
                Junction(),
                Resistor(20),
                Resistor(40),
                Resistor(30),
                Resistor(60),
                Junction(),
                Junction(),
                Multimeter(Meter_Type.VOLTMETER),
                Junction()
            ],
            [
                Wire(0, 1),
                Wire(1, 2),
                Wire(1, 4),
                Wire(2, 6),
                Wire(6, 3),
                Wire(6, 8),
                Wire(4, 7),
                Wire(7, 8),
                Wire(7, 5),
                Wire(3, 9),
                Wire(5, 9),
                Wire(9, 0)
            ]
        ]),

        "c14": np.array([
            [
                DC_Battery(1),
                Junction(4),
                Junction(),
                Junction(),
                Junction(),
                Junction(),
                Junction(),
                Junction(),
                Junction(4),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Resistor(1),
                Multimeter(Meter_Type.AMMETER)
            ],
            [
                Wire(0, 1),
                Wire(0, 21),
                Wire(21, 8),
                Wire(1, 9),
                Wire(1, 12),
                Wire(1, 13),
                Wire(2, 9),
                Wire(2, 10),
                Wire(2, 14),
                Wire(3, 10),
                Wire(3, 11),
                Wire(3, 15),
                Wire(4, 11),
                Wire(4, 12),
                Wire(4, 16),
                Wire(5, 16),
                Wire(5, 17),
                Wire(5, 20),
                Wire(6, 13),
                Wire(6, 17),
                Wire(6, 18),
                Wire(7, 14),
                Wire(7, 18),
                Wire(7, 19),
                Wire(8, 15),
                Wire(8, 19),
                Wire(8, 20)
            ]
        ]),

        "c15": np.array([
            [
                DC_Battery(7.8),
                Resistor(1001),
                Junction(),
                Resistor(99.9),
                DC_Battery(2.548),
                Junction(),
                Resistor(2012)
            ],
            [
                Wire(0, 1),
                Wire(5, 0),
                Wire(4, 3),
                Wire(5, 4),
                Wire(1, 2),
                Wire(2, 3),
                Wire(2, 6),
                Wire(6, 5)
            ]
        ])
    }

    if data_key == "all":
        # special arg to return all files
        files = []
        for key in data.keys():
            files.append(data[key])
        return files
    elif data_key in data.keys():
        np.save(data_key, data[data_key])
        #could actually just return the array
        return 0
    else:
        return 1
