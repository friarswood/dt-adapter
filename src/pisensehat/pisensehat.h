#pragma once

#include "common/sensor.h"

#ifdef HAVE_PISENSEHAT
#include "RTIMULib.h"
#else
#include "RTIMULib_stub.h"
#endif

#include <string>

class PiSenseHat final : public Sensor
{
public:

  struct Status
  {
    typedef int value;
    static const value OK = 0;
    static const value NO_PRESSURE = 1;
    static const value NO_HUMIDITY = 2;
    static const value NO_IMU = 4;
  };

  py::str id() const override;
  py::str type() const override;
  py::str status() const override;
  py::dict read() override;

  PiSenseHat();

  ~PiSenseHat();

  PiSenseHat(const PiSenseHat&) = delete;
  PiSenseHat(PiSenseHat&&) = delete;
  PiSenseHat& operator=(const PiSenseHat&) = delete;
  PiSenseHat& operator=(PiSenseHat&&) = delete;

  static std::string statusToString(PiSenseHat::Status::value status);

private:

  std::string m_id;
  std::unique_ptr<RTIMUSettings> m_settings;
  std::unique_ptr<RTIMU> m_imu;
  std::unique_ptr<RTPressure> m_pressure;
  std::unique_ptr<RTHumidity> m_humidity;
  Status::value m_status;
};

