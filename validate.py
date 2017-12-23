bounds = {
    "Resistor": {"resistance": [1e-6, 1e4]},
    "DC_Battery": {"voltage": [1e-03, 1e4]},
    "Light_Bulb": {"resistance": [1e-6, 1e4], "wattage": [1e-6, 1e6]},
    "Junction": {"num_cxns": [3, 4]},
    "Voltmeter": {},
    "Ammeter": {},
    "Capacitor": { "voltage": [1e-3, 1e3], "capacitance": [1e-3, 1e4]},
    "Switch": {"state": ["ON", "OFF"]}
}


def validate_bounds(data):
    comp = bounds[data['type']]

    validation = {}

    if comp == "Junction" or comp == "Switch":
        key = comp.keys()[0]
        validation[key] = data[key] in comp[key]
        return validation        

    for key in comp.keys():
        if comp[key][0] <= float(data[key]) <= comp[key][1]:
            validation[key] = True
        #special case
        elif comp == "Capacitor" and key == "voltage" and val == 0:
            validation[key] = True
        else:
            validation[key] = False

    return validation
