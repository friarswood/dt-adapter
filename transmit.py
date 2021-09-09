import dt_adapter

import os
from time import sleep
import disruptive as dt
import argparse

import logging
logging.captureWarnings(True)
FORMAT = '%(asctime)s; %(levelname)s; %(funcName)s [%(filename)s:%(lineno)s]; %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


def run(module, class_, update_period):
  project_id = os.getenv("DT_PROJECT")
  svc_key = os.getenv("DT_SVC_KEY")
  svc_secret = os.getenv("DT_SVC_SECRET")
  svc_email = os.getenv("DT_SVC_EMAIL")

  dt.default_auth = dt.Auth.service_account(svc_key, svc_secret, svc_email)

  sensor = dt_adapter.get_driver(module, class_)

  dt_adapter.startup(project_id, sensor.type())

  label_filters = {"provider": "friarswood", "virtual-sensor": "", "type": sensor.type(), "external_id": sensor.id()}
  while True:
    try:
      vsensors = dt.Device.list_devices(project_id, label_filters=label_filters)

      reading = sensor.read()
      status_msg = f"sensor status={reading['status']} @ {reading['timestamp']}"
      logging.info(status_msg)

      if not vsensors:
        logging.error(f"no virtual sensor found for {sensor.type()} {sensor.id()}")

      for vs in vsensors:
        if reading["status"] == "OK":
          if vs.labels["virtual-sensor"] == "pressure" and vs.device_type == "temperature":
            data = dt.events.Temperature(celsius=reading["pressure"], timestamp=reading["timestamp"])
          elif vs.labels["virtual-sensor"] == "humidity" and vs.device_type == "humidity":
            data = dt.events.Humidity(celsius=reading["temperature"], relative_humidity=reading["humidity"], timestamp=reading["timestamp"])
          else:
            continue
          logging.info(f"updating {vs.device_id}")
          err = dt.Emulator.publish_event(vs.device_id, project_id, data=data)
          assert not err, str(err)
        else:
          err = dt.Device.set_label(vs.device_id, project_id, "error", status_msg)
          assert not err, str(err)

    except Exception as e:
      logging.error(f"{e.__class__.__name__}: {str(e)}")
    sleep(update_period)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="push sensor readings to DT cloud")
  parser.add_argument("-m", "--module", type=str, required=True, help="sensor module name")
  parser.add_argument("-c", "--class", type=str, required=True, help="sensor driver class name")
  parser.add_argument("-u", "--update", type=int, required=True, help="update period (seconds)")
  args = parser.parse_args()

  print(args)
  run(args.module, getattr(args,"class"), args.update)
