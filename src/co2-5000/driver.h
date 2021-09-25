#pragma once

#include <pybind11/pybind11.h>

#include <array>
#include <string>

namespace py = pybind11;

typedef unsigned char byte;

std::array<uint8_t, 2> calc_crc(const uint8_t *data, size_t len);
bool check_crc(const uint8_t *data, size_t len);

class CO2_5000 final
{
public:
  static const size_t MSG_LEN = 9;

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
  std::array<byte, MSG_LEN> m_response_buffer;
};

