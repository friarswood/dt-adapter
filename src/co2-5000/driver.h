#pragma once

#include <pybind11/pybind11.h>

#include <array>
#include <string>

namespace py = pybind11;

std::array<uint8_t, 2> calc_crc(const uint8_t *data, size_t len);
bool check_crc(const uint8_t *data, size_t len);

class CO2_5000 final
{
public:

  // Errors detectred on host (see datasheet for errors trapped on device)
  static const uint8_t OK = 0x0;
  static const uint8_t WRITE_FAILED = 0x81;
  static const uint8_t READ_FAILED = 0x82;
  static const uint8_t INVALID_CRC = 0x83;
  static const uint8_t INVALID_DATA = 0x84;


  CO2_5000();

  ~CO2_5000() = default;

  CO2_5000(const CO2_5000&) = delete;
  CO2_5000(CO2_5000&&) = delete;
  CO2_5000& operator=(const CO2_5000&) = delete;
  CO2_5000& operator=(CO2_5000&&) = delete;

  py::str id() const;
  py::str type() const;
  py::str status() const;
  py::dict reading();

private:
  std::string m_id;
  int m_fd;
  uint8_t m_status;
};

