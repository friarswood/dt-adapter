import dt_adapter

from dotenv import load_dotenv
from time import sleep
import argparse
import json
import requests

import logging
logging.captureWarnings(True)
FORMAT = '%(asctime)s; %(levelname)s; %(funcName)s [%(filename)s:%(lineno)s]; %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

load_dotenv()


def run(module, class_, url, update_period):

  sensor = dt_adapter.get_driver(module, class_)

  data = {
    "id": sensor.id(),
    "device": sensor.type(),
    "value": None,
    "timestamp": None
  }

  # label_filters = {"provider": "friarswood", "virtual-sensor": "", "type": sensor.type(), "external_id": sensor.id()}
  while True:
    try:
      data["value"] = sensor.read()
      data["timestamp"] = data["value"]["timestamp"]

      print(data)

      payload = json.dumps(data).encode("utf-8")

      response = requests.post(url, data=payload, headers={"x-fw-signature": dt_adapter.make_token(payload), "Content-Type": "application/json"})
      print(f"{data['value']['timestamp']}: {response.status_code} {response.text}")

    except Exception as e:
      logging.error(f"{e.__class__.__name__}: {str(e)}")

    sleep(update_period)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="push sensor readings to virtual cloud connector")
  parser.add_argument("-m", "--module", type=str, required=True, help="sensor module name")
  parser.add_argument("-c", "--class", type=str, required=True, help="sensor driver class name")
  parser.add_argument("-s", "--server", type=str, required=True, help="virtual cloud connector url")
  parser.add_argument("-u", "--update", type=int, required=True, help="update period (seconds)")

  args = parser.parse_args()

  print(args)
  run(args.module, getattr(args, "class"), args.server, args.update)
