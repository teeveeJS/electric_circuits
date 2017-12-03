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
                Resistor(50),
                Resistor(50),
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
        "c5": np.array([
            [
                DC_Battery(12),
                Resistor(5),
                DC_Battery(12),
                Resistor(5)
            ],
            [
                Wire(0, 1),
                Wire(1, 0),
                Wire(2, 3),
                Wire(3, 2)
            ]
        ]),
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
        ])
    }

    np.save(data_key, data[data_key]) #could actually just return the array
