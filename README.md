# dt-adapter

Demonstration of a software adapter to give external sensor support in DT Studio.

External sensor is a Raspberry Pi + Sense Hat (Pressure, temperature, humidity, accelerometer, compass)

Periodicially broadcasts readings to emulated devices in DT studio, using labels to identify the device:

`external_id: pisensehat`

`virtual-sensor: humidity, pressure`

