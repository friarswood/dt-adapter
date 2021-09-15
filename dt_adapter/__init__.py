__version__ = "2.0.0"

import os
import _pisensehat as pisensehat
import mh_z19
from importlib import import_module
from hashlib import sha1
import jwt


from dotenv import load_dotenv
load_dotenv()


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