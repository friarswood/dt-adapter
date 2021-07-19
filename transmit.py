
import os
from time import sleep
import disruptive as dt

import logging
logging.captureWarnings(True)
FORMAT = '%(asctime)s; %(levelname)s; %(funcName)s [%(filename)s:%(lineno)s]; %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

import dt_adapter

def main():

  project_id = os.getenv("DT_PROJECT")
  svc_key = os.getenv("DT_SVC_KEY")
  svc_secret = os.getenv("DT_SVC_SECRET")
  svc_email = os.getenv("DT_SVC_EMAIL")

  dt.default_auth = dt.Auth.service_account(svc_key, svc_secret, svc_email)

  pisensehat = dt_adapter.PiSenseHat()

  label_filters={"virtual-sensor": "", "type": dt_adapter.SENSOR_NAME, "external_id": dt_adapter.get_device_id()}
  while True:
    try:
      vsensors = dt.Device.list_devices(project_id, label_filters=label_filters)

      reading = pisensehat.read()
      status_msg = f"sensor status={reading['status']} @ {reading['timestamp']}"
      logging.info(status_msg)

      for vs in vsensors:
        if reading["status"] == "OK":
          if vs.labels["virtual-sensor"] == "pressure" and vs.device_type == "temperature":
            data = dt.events.Temperature(celsius=reading["pressure"], timestamp=reading["timestamp"])
          elif vs.labels["virtual-sensor"] == "humidity" and vs.device_type == "humidity":
            data = dt.events.Humidity(celsius=reading["temperature"], relative_humidity=reading["humidity"], timestamp=reading["timestamp"])
          else:
            continue
          logging.info("updating %s" % vs.device_id)
          err = dt.Emulator.publish_event(vs.device_id, project_id, data=data)
          assert not err, str(err)
        else:
          err = dt.Device.set_label(vs.device_id, project_id, "error", status_msg)
          assert not err, str(err)

      sleep(dt_adapter.UPDATE_PERIOD)
    except Exception as e:
      logging.error(f"{e.__class__.__name__}: {str(e)}")


if __name__ == "__main__":
  main()
