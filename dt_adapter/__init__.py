__version__ = "0.0.0"

from _pisensehat import PiSenseHat
from dotenv import load_dotenv

SENSOR_NAME = "pisensehat"
UPDATE_PERIOD = 10*60
load_dotenv()


def get_device_id():
  try:
    with open("/proc/device-tree/hat/uuid", "r") as fd:
      return fd.read().rstrip("\x00")
  except:
    return "00000000-0000-0000-0000-000000000000"

