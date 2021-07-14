# dt-adapter

Demonstration of a software adapter to give external sensor support in DT Studio.

External sensor is a Raspberry Pi + Sense Hat (Pressure, temperature, humidity, accelerometer, compass)

Periodicially broadcasts readings to emulated devices in DT studio, using labels to identify the device:

`external_id: pisensehat`

`virtual-sensor: humidity, pressure`


## developing on platform with no sensor

(Ras Pi 3 is very slow and only has console access.)

You can stub the sensor if necessary by setting the SENSOR_STUB env var (to any value)

e.g

```sh
SENSOR_STUB=1 python setup.py develop
```

or

```
SENSOR_STUB=1 pip install -e .
```
