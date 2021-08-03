import os
import atexit
import signal
import logging

import disruptive as dt


vccon_id = None

project_id_global = None


def get_device_id():
  try:
    with open("/proc/device-tree/hat/uuid", "r") as fd:
      return fd.read().rstrip("\x00")
  except Exception:
    return "00000000-0000-0000-0000-000000000000"


def startup(project_id, device_type):

  global project_id_global
  project_id_global = project_id  # for shutdown

  global vccon_id

  host = os.getenv("FW_HOST")
  ip = os.getenv("FW_IP")

  # skip if running in a dev/ci env
  if host == "dev" or device_type == "IMU-STUB":
    return

  # create the "driver" if it doesnt exist
  labels = {"provider": "friarswood", "virtual-sensor": "3rd-party"}
  # print("starting up")
  driver = dt.Device.list_devices(project_id, device_types=[dt.Device.CLOUD_CONNECTOR], label_filters=labels)
  if not driver:
    driver = [dt.Emulator.create_device(project_id, device_type=dt.Device.CLOUD_CONNECTOR, display_name="Fw3rdPartySensorDriver", labels=labels)]
  vccon_id = driver[0].device_id

  # register function to call if terminating (ctrl-C)
  atexit.register(shutdown)
  # register function to call if terminated (kill <pid>)
  signal.signal(signal.SIGTERM, shutdown_sig)

  network = dt.events.EthernetStatus(host, ip)
  res = dt.Emulator.publish_event(device_id=vccon_id, project_id=project_id, data=network)
  assert not res

  connection = dt.events.ConnectionStatus(connection="ETHERNET", available=["ETHERNET"])
  res = dt.Emulator.publish_event(device_id=vccon_id, project_id=project_id, data=connection)
  assert not res


def shutdown():
  global vccon_id
  global project_id_global
  logging.info("shutting down")
  if vccon_id:
    connection = dt.events.ConnectionStatus(connection="OFFLINE", available=["ETHERNET"])
    res = dt.Emulator.publish_event(device_id=vccon_id, project_id=project_id_global, data=connection)
    assert not res


def shutdown_sig(_signum, _frame):
  shutdown()
  exit(1)
