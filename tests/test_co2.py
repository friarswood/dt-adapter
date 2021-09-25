from dt_adapter import get_driver


def test_co2_5000():

  module = "dt_adapter"
  class_ = "co2_5000.Sensor"

  sensor = get_driver(module, class_)

  assert sensor.type().startswith("CO2-5000")

  assert sensor.id() == "testing123"
  assert sensor.status() == "OK"

  readings = sensor.read()

  assert isinstance(readings, dict)

  print(readings)

  assert "status" in readings and readings["status"] == "OK"
  assert "timestamp" in readings
  assert "co2" in readings


def test_co2_5000_crc():

  from dt_adapter import co2_5000

  msg = bytes.fromhex("646901") # get co2
  msg += co2_5000.crc(msg)
  assert msg.hex()[-4:] == "df8f"
  assert co2_5000.check_crc(msg)

  msg = bytes.fromhex("646902") # get temp
  msg += co2_5000.crc(msg)
  assert msg.hex()[-4:] == "9f8e"
  assert co2_5000.check_crc(msg)

  # wrong crc
  msg = bytes.fromhex("646902df8f")
  assert not co2_5000.check_crc(msg)


if __name__ == "__main__":
  #test_co2_5000()
  test_co2_5000_crc()
