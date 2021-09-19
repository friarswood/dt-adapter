from dt_adapter import get_driver


def test_mh_z19():

  module = "dt_adapter"
  class_ = "mh_z19c.Sensor"

  sensor = get_driver(module, class_)

  assert sensor.type().startswith("MH-Z19C")

  assert sensor.id() == "testing123"
  assert sensor.status() == "OK"

  readings = sensor.read()

  assert isinstance(readings, dict)

  print(readings)

  assert "status" in readings and readings["status"] == "OK"
  assert "timestamp" in readings
  assert "co2" in readings


if __name__ == "__main__":
  test_mh_z19()
