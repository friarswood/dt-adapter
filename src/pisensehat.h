#pragma once

#include "RTIMULib.h"

#include <pybind11/pybind11.h>

#include <string>

namespace py = pybind11;

class PiSenseHat
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

  py::dict read() const;

  PiSenseHat();

  ~PiSenseHat();

  PiSenseHat(const PiSenseHat&) = delete;
  PiSenseHat(PiSenseHat&&) = delete;
  PiSenseHat& operator=(const PiSenseHat&) = delete;
  PiSenseHat& operator=(PiSenseHat&&) = delete;

  static std::string statusToString(PiSenseHat::Status::value status);

private:

  std::unique_ptr<RTIMUSettings> m_settings;
  std::unique_ptr<RTIMU> m_imu;
  std::unique_ptr<RTPressure> m_pressure;
  std::unique_ptr<RTHumidity> m_humidity;
  Status::value m_status;
};

