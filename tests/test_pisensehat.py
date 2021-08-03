import os
from dt_adapter import PiSenseHat, get_device_id


def test_pisensehat():

  pisensehat = PiSenseHat()

  if os.getenv("SENSOR_STUB"):
    assert pisensehat.type() == "IMU-STUB"
  else:
    assert pisensehat.type() == "LSM9DS1"

  assert get_device_id() == pisensehat.id()
  assert pisensehat.status() == "OK"

  readings = pisensehat.read()

  print(readings)

  assert "status" in readings and readings["status"] == "OK"
  assert "timestamp" in readings
  assert "temperature" in readings
  assert "humidity" in readings
  assert "pressure" in readings


if __name__ == "__main__":
  test_pisensehat()
