__version__ = "1.0.0"

from .startup import startup
import _pisensehat as pisensehat
from dotenv import load_dotenv
import mh_z19
from importlib import import_module

load_dotenv()


def get_driver(module, class_):
  m = import_module(module)
  c = m
  for s in class_.split("."):
    c = getattr(c, s)
  return c()
