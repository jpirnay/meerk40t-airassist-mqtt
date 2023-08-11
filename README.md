# meerk40t-airassist-mqtt
Plugin to add mqtt coolant support for MeerK40t 0.9 and higher

# Introduction
MeerK40t (https://github/meerk40t/meerk40t) has introduced since v0.9 an option to add plugins to provide airassist / coolant functionality. By default it offers just basic functionality though.

This plugin allows to turn on or off an external device via the use of mqtt commands. A simple application is an aquarium pump with one of the popular smart plugs (eg based on the tasmota firmware (https://github.com/arendst/Tasmota))

# Installing
* `pip install meerk40t-airassist-mqtt`
Or
* Download into a directory:
* `$ pip install .`

# Development

* If you are developing your own extension for meerk40t you will want to use:
* `$ pip install -e .` this installs the python module in edit mode which allows you to easily see and experience your changes. Without reinstalling your module.

# Acknowledgements

* This MeerK40t extension uses the work of a great library to use the mqtt protocol: https://github.com/eclipse/paho.mqtt.python