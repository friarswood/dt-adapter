
from serial import Serial
from time import sleep
import struct
from dt_adapter import co2_5000
from datetime import datetime

port = "/dev/serial0"
baud = 9600

# converts hex string to bytes and appends CRC
def make_msg(hexstr):
  b = bytes.fromhex(hexstr)
  return b + co2_5000.crc(b)

# READ_SETTINGS = bytes.fromhex("fe03040001005165")
READ_CO2 = bytes.fromhex("646901DF8F")
READ_TEMP = make_msg("646902")
# READ_CO2_I = bytes.fromhex("6469035E4E")
GET_REF_PARAM = bytes.fromhex("646801DE1F") # returns 64e801.... = "Illegal function"
#SET_REF_PARAM
SELFCAL_STATUS = make_msg("642767")
SELFCAL_PERIOD = make_msg("642769")


def start_calibration_msg(conc):
  assert conc >= 400.0 and conc <= 5000.0
  b = bytes.fromhex("64 27 80") + struct.pack("<f", conc)
  crc = co2_5000.crc(b)
  return b + crc
# device returns FE2780xxxxxxxxsscccc where ss=01 for success FF for error


QUERY_CALIBRATION = bytes.fromhex("642781")
QUERY_CALIBRATION += co2_5000.crc(QUERY_CALIBRATION)
# device returns FE2781sscccc where ss=01 for started 00 for finished


# serial write, check, serial read, check, return
def write_read(ser, msg, response_len):
  written = ser.write(msg)
  assert written == len(msg), f"error {written}/{len(msg)} bytes written"
  resp = ser.read(response_len)
  assert len(resp) == response_len, f"error {len(resp)}/{response_len} bytes read"
  assert co2_5000.check_crc(resp), f"response '{resp.hex()}' crc is invalid"
  return resp

# setting 400ppm calibration gives:
#64 27 80 0000c843 ff ff9c
#                  ^^ error code

try:

  # # try to read a line of data from the serial port and parse
  with Serial(port, baudrate=baud, timeout=1.0) as ser:

    sleep(0.1)
    msg = SELFCAL_STATUS
    resp = write_read(ser, msg, 6)
    print(msg.hex(), resp.hex())
    #assert resp[8] == b"\x01", f"calibration did not start. response: {resp.hex()}"
    print(f"{datetime.now().isoformat()} Self-calibration status: {resp[3:4].hex()}")

    sleep(0.1)
    msg = SELFCAL_PERIOD
    resp = write_read(ser, msg, 7)
    print(msg.hex(), resp.hex())
    #assert resp[8] == b"\x01", f"calibration did not start. response: {resp.hex()}"
    print(f"{datetime.now().isoformat()} Self-calibration period: {struct.unpack('<H', resp[3:5])[0]}")

    sleep(0.1)
    msg = start_calibration_msg(413.0)
    resp = write_read(ser, msg, 10)
    assert resp[8] == 1, f"calibration did not start. response: {resp.hex()}"
    ppm = struct.unpack("<f", resp[4:8])[0]
    print(f"{datetime.now().isoformat()} Calibration @{ppm:.1f}ppm started...")

    while True:
      sleep(300)
      # check if calibration finished
      resp = write_read(ser, QUERY_CALIBRATION, 6)
      if resp[3] == b"\00":
        break
      print(f"{datetime.now().isoformat()} Calibrating...")
    print(f"{datetime.now().isoformat()} Calibration complete")

except Exception as e:
  print(f"{datetime.now().isoformat()} {e}")