# Interactive Simulation of Electric Circuits
A responsive program where the user will directly interface with an electric circuit, controlling its connections, components, and their values. The available components include, but are not necessarily limited to, voltage sources, switches, resistors, capacitors, and inductors. The user will be able to construct unique circuits from the above-mentioned components or explore various basic circuits, such as RC and LC circuits.

In terms of code, the program will use:
* Kirchhoff's Loop Rules
	* Matrices and linear algebra to solve systems of equations
* Numerical approximations to differential equations
	* To model the behavior of capacitors and inductors
* Object-oriented programming to organize the components and their properties
* A Python GUI (such as TKinter) to interface between the user and the program
* Matplotlib.pyplot to represent various data from the circuits
	* A graph of Current vs. Time in a RC circuit, for instance
* And undoubtedly more!


## Usage
To start, run
`python main.py`
You can choose between loading a pre-existing circuit or manually entering the circuit data by either entering 1 or the number of components in your desired circuit, respecitvely. The pre-existing files have names c1 through c13.
~~~~
Enter 1 to load Circuit from file
How many components will the circuit contain?
>>3
~~~~
Currently, the components you can choose from are Batter, Resistor, Junction, and Capacitor.
~~~~
(0) What kind of component?
>>battery
Please enter voltage.
>>12
(1) What kind of component?
>>resistor
Please enter resistance.
>>1000
(2) What kind of component?
>>capacitor
Please enter capacitance (microfarads).
>>100
~~~~
Once you have inputted the necessary component data, you will be prompted to connect the components by entering the components' IDs, which are printed to the left of each component.
~~~~
==========
COMPONENTS
==========
0 <components.DC_Battery object at 0x7f2bcb5352b0>
1 <components.Resistor object at 0x7f2bcb535240>
2 <components.Capacitor object at 0x7f2bc23fb898>
Enter start point.
>>0
Enter end point.
>>1
~~~~
Once you have entered all of the connections, you can save the circuit by entering 'y'. Then the circuit will be created and the values calculated.
~~~~
============
Circuit Data
============
0 <class 'components.DC_Battery'> I: [ -3.54151985e-07] V: 12.0 R: 0
1 <class 'components.Resistor'> I: [  3.54151985e-07] V: [ 0.00035415] R: 1000.0
2 <class 'components.Capacitor'> I: [  3.54151985e-07] V: [ 11.99968126] R: 0
============
~~~~

