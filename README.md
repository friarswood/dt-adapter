# dt-adapter

[![build, lint and test](https://github.com/friarswood/dt-adapter/actions/workflows/build-lint-test.yaml/badge.svg)](https://github.com/friarswood/dt-adapter/actions/workflows/build-lint-test.yaml)

Demonstration of a software adapter to give 3rd party sensor support in DT Studio.

External sensor is a Raspberry Pi + Sense Hat (Pressure, temperature, humidity, accelerometer, compass)

Periodicially broadcasts readings to emulated devices in DT studio, using the following labels to identify the device:

`type: LSM9DS1`
`external_id: f159fb28-5a70-4afc-9a8e-aab9e88354f7`
`provider: friarswood`

and either

`virtual-sensor: pressure`

or

`virtual-sensor: humidity`

for humidity and temperature readings.
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

Tests must be run with this too:

SENSOR_STUB=1 pytest
