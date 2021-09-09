import os
from dt_adapter import mh_z19

# def get_device_id():
#   try:
#     with open("/proc/device-tree/hat/uuid", "r") as fd:
#       return fd.read().rstrip("\x00")
#   except Exception:
#     return "00000000-0000-0000-0000-000000000000"



def test_mh_z19():

  sensor = mh_z19.Sensor()

  # if os.getenv("SENSOR_STUB"):
  #   assert sensor.type() == "IMU-STUB"
  # else:

  assert sensor.type() == "MH-Z19"


  assert sensor.id() == "0000"
  assert sensor.status()

  readings = sensor.read()

  assert isinstance(readings, dict)

  # print(readings)

  # assert "status" in readings and readings["status"] == "OK"
  # assert "timestamp" in readings
  # assert "temperature" in readings
  # assert "humidity" in readings
  # assert "pressure" in readings


if __name__ == "__main__":
  test_mh_z19()
