from dt_adapter import pisensehat

def test_pisensehat():

  readings = pisensehat.read()

  assert "status" in readings and readings["status"] == "OK"
  assert "temperature" in readings
  assert "humidity" in readings
  assert "pressure" in readings


