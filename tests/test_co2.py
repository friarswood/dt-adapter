from dt_adapter import get_driver


def test_mh_z19():

  module = "dt_adapter"
  class_ = "mh_z19.Sensor"

  sensor = get_driver(module, class_)

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
