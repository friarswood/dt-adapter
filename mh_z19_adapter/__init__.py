
from datetime import datetime

try:
  import mh_z19

  class Sensor:
    """ CO2 sensor """
    def __init__(self):
      pass

    def id(_self) -> str:
      return "TODO..."

    def type(_self) -> str:
      return "MH-Z19C"

    def status(_self) -> str:
      return "TODO..."

    def read(self) -> dict:
      return {**mh_z19.read(), **{"timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}}


# if no mh-z19 module, use the stub
except ImportError:

  import numpy as np

  class Sensor:
    """ CO2 sensor stub """
    def __init__(self):
      self.ppm = 400.0

    def id(_self) -> str:
      return "testing123"

    def type(_self) -> str:
      return "MH-Z19C"

    def status(_self) -> str:
      return "OK"

    def read(self) -> dict:
      self.ppm += np.random.normal(0.0, 5.0)
      return {"co2": self.ppm, "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
