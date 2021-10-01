
import dt_adapter

def test_dummy():


  class Dummy(dt_adapter.Sensor):

    def __init__(self):
      super().__init__()

    def type(self):
      return "dummy"

    def id(self):
      return "dummy01"

    def status(self):
      return "OK"

    def read(self):
      return {"dummy": 0, "timestamp": dt_adapter.utc_now()}

  s = Dummy()

  assert s.type() == "dummy"
  assert s.id() == "dummy01"
  assert s.status() == "OK"
  reading = s.read()
  assert reading["dummy"] == 0
  assert "timestamp" in reading

