
import os
from datetime import date, datetime
from time import sleep
import disruptive as dt
from dotenv import load_dotenv

import numpy as np
rng = np.random.default_rng()
t = 20.0

def fake_reading():
  return {
    "status": "OK",
    "temperature": 20.0 + rng.random(),
    "pressure": 1000.0 + rng.random() * 10,
    "humidity": 50.0 + rng.random() * 10,
    "timestamp": datetime.utcnow()
  }

SENSOR_NAME = "pisensehat"
UPDATE_PERIOD = 10*60
load_dotenv()


def main():

  project_id = os.getenv("DT_PROJECT")
  svc_key = os.getenv("DT_SVC_KEY")
  svc_secret = os.getenv("DT_SVC_SECRET")
  svc_email = os.getenv("DT_SVC_EMAIL")

  dt.default_auth = dt.Auth.service_account(svc_key, svc_secret, svc_email)

  while True:

    sensors = dt.Device.list_devices(project_id, label_filters={"virtual-sensor": "", "external_id": SENSOR_NAME})

    reading = fake_reading()

    for s in sensors:
      print(s.device_id)
      if s.labels["virtual-sensor"] == "pressure" and s.device_type == "temperature":
        data = dt.events.Temperature(celsius=reading["pressure"], timestamp=reading["timestamp"])
      elif s.labels["virtual-sensor"] == "humidity" and s.device_type == "humidity":
        data = dt.events.Humidity(celsius=reading["temperature"], relative_humidity=reading["humidity"], timestamp=reading["timestamp"])
      else:
        print(s)
        continue
      print(data)
      err = dt.Emulator.publish_event(s.device_id, project_id, data=data)
      assert not err, str(err)



    sleep(UPDATE_PERIOD)


if __name__ == "__main__":
  main()
