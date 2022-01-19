# dt-adapter

[![build, lint and test](https://github.com/friarswood/dt-adapter/actions/workflows/build-lint-test.yaml/badge.svg)](https://github.com/friarswood/dt-adapter/actions/workflows/build-lint-test.yaml)

Transmits signed sensor readings to a [`dt-vccon`]() virtual cloud connector. Use like so:

```sh
python transmit.py -m <module> -c <class> -u <update-time> -s <vccon-url>
```



## Pisensehat

The adapter reads pressure, temperature, and humidity and forwards to the virtual cloud connector, which will pass the temperature and humidity readings on to a virtual humidity sensor, and the pressure reading to a virtual temperature sensor<sup>&ast;</sup>.

```sh
python transmit.py -m dt_adapter -c pisensehat.Sensor -u 300 -s https://fw-dt-vccon.azurewebsites.net/incoming
```
## CO2-5000

This reads CO<sub>2</sub> concentration and and forwards to the virtual cloud connector, which will pass the reading on to a virtual temperature sensor<sup>&ast;</sup>.

```sh
python transmit.py -m dt_adapter -c mh_z19_adapter.Sensor -u 300 -s https://fw-dt-vccon.azurewebsites.net/incoming
```

&ast; the virtual sensor must be labelled with the type and id of the corresponding physical device.

## Developing on platform with no sensor

This is the default. Sensors are stubbed and return dummy readings.(Ras Pi can be very slow and only have console access.)

You can enable the actual sensor if necessary by setting the appropriate env var (to any value)

e.g

```sh
HAVE_PISENSEHAT=1 python setup.py develop
```

or

```
HAVE_CO2_5000=1 python setup.py develop
```
