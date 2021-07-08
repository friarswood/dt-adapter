
import os
from datetime import date, datetime
from time import sleep
import disruptive as dt

import dt_adapter


def main():

  project_id = os.getenv("DT_PROJECT")
  svc_key = os.getenv("DT_SVC_KEY")
  svc_secret = os.getenv("DT_SVC_SECRET")
  svc_email = os.getenv("DT_SVC_EMAIL")

  dt.default_auth = dt.Auth.service_account(svc_key, svc_secret, svc_email)

  stub = dt_adapter.stub.Sensor()

  while True:

    sensors = dt.Device.list_devices(project_id, label_filters={"virtual-sensor": "", "external_id": dt_adapter.SENSOR_NAME})

    reading = stub.read()
    status_msg = f"sensor status={reading['status']} @ {reading['timestamp']}"
    print(status_msg)

    for s in sensors:
      if reading["status"] == "OK":
        if s.labels["virtual-sensor"] == "pressure" and s.device_type == "temperature":
          data = dt.events.Temperature(celsius=reading["pressure"], timestamp=reading["timestamp"])
        elif s.labels["virtual-sensor"] == "humidity" and s.device_type == "humidity":
          data = dt.events.Humidity(celsius=reading["temperature"], relative_humidity=reading["humidity"], timestamp=reading["timestamp"])
        else:
          continue
        print("updating %s" % s.device_id)
        err = dt.Emulator.publish_event(s.device_id, project_id, data=data)
        assert not err, str(err)
      else:
        err = dt.Device.set_label(s.device_id, project_id, "error", status_msg)
        assert not err, str(err)

    sleep(dt_adapter.UPDATE_PERIOD)


if __name__ == "__main__":
  main()
