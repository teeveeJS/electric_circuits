from components import *


def create_samples():
    # a very simple circuit
    c1 = np.array([
        [
            DC_Battery(12),
            Resistor(5)
        ],
        [
            Wire(0, 1),
            Wire(1, 0)
        ]
    ])
    np.save("c1", c1)


    # a more complex circuit
    c2 = np.array([
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
    ])
    np.save("c2", c2)


    # basic RC circuit
    c3 = np.array([
        [
            Capacitor(100, v_init=12),
            Resistor(1000)
        ],
        [
            Wire(0, 1),
            Wire(1, 0)
        ]
    ])
    np.save("c3", c3)


    # charging a capacitor
    c4 = np.array([
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
    ])
    np.save("c4", c4)
