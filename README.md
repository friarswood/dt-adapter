# dt-adapter

Demonstration of a software adapter to give external sensor support in DT Studio.

External sensor is a Raspberry Pi + Sense Hat (Pressure, temperature, humidity, accelerometer, compass)

Periodicially broadcasts readings to emulated devices in DT studio, using labels to identify the device:

`external_id: pisensehat`

`virtual-sensor: humidity, pressure`


## developing on platform with no sensor

(Ras Pi 3 is very slow and only has console access.) 

You can stub the sensor if necessary. In pisensehat.h, change

```cpp
#include "RTIMULib.h"
```

to

```cpp
#include "RTIMULib_stub.h"
```

And in setup.py comment out the line

```python
extra_link_args = ['-lRTIMULib']
```

and comment out this while condition in `pisensehat::read`, otherwise will get stuck in an infinite loop

```cpp
  while (!(m_status & Status::NO_IMU) && m_imu->IMURead())
```