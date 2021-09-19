import os
from dt_adapter import get_driver


def get_device_id():
  try:
    with open("/proc/device-tree/hat/uuid", "r") as fd:
      return fd.read().rstrip("\x00")
  except Exception:
    return "00000000-0000-0000-0000-000000000000"


def test_pisensehat():

  module = "dt_adapter"
  class_ = "pisensehat.Sensor"

  sensor = get_driver(module, class_)

  if os.getenv("HAVE_PISENSEHAT"):
    assert sensor.type() == "LSM9DS1"
  else:
    assert sensor.type() == "IMU-STUB"

  assert sensor.id() == get_device_id()
  assert sensor.status() == "OK"

  readings = sensor.read()

  print(readings)

  assert "status" in readings and readings["status"] == "OK"
  assert "timestamp" in readings
  assert "temperature" in readings
  assert "humidity" in readings
  assert "pressure" in readings


if __name__ == "__main__":
  test_pisensehat()
