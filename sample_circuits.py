from components import *


def create_samples():
    c1 = np.array([
        [
            DC_Battery(0, 12),
            Resistor(1, 5)
        ],
        [
            Wire(0, 1),
            Wire(1, 0)
        ]
    ])
    np.save("c1", c1)


    c2 = np.array([
        [
            DC_Battery(0, 100),
            Junction(1),
            Junction(2),
            Resistor(3, 50),
            Resistor(4, 50),
            Resistor(5, 50),
            Junction(6),
            Junction(7)
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
