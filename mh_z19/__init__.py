
# import mh_z19

class Sensor:
  """ CO2 sensor """
  def __init__(self):
    pass

  def id(_self) -> str:
    return "0000"

  def type(_self) -> str:
    return "MH-Z19"

  def status(_self) -> str:
    return "?"

  def read(_self) -> dict:
    return {"co2_ppm": 100}
