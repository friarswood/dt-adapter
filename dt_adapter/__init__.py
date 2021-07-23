__version__ = "0.1.0"

from .startup import startup, get_device_id
from _pisensehat import PiSenseHat
from dotenv import load_dotenv

SENSOR_NAME = "pisensehat"
UPDATE_PERIOD = 10*60
load_dotenv()
