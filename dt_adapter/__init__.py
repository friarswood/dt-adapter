__version__ = "2.0.1"

import os
try:
  from _common import *
except ImportError as e:
  print(e)
try:
  import _pisensehat as pisensehat
except ImportError as e:
  print(e)
try:
  import _co2_5000 as co2_5000
except ImportError as e:
  print(e)
from importlib import import_module
from hashlib import sha1
import jwt


def get_driver(module, class_):
  m = import_module(module)
  c = m
  for s in class_.split("."):
    c = getattr(c, s)
  return c()


def make_token(data):
  m = sha1()
  m.update(data)
  return jwt.encode({"checksum": m.digest().hex()}, os.getenv("FW_VCCON_SIGNATURE_SECRET"), algorithm="HS256")
