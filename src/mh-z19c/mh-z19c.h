#pragma once

#include <pybind11/pybind11.h>

#include <string>

namespace py = pybind11;

typedef unsigned char byte;


class MH_Z19C final
{
public:
  static const size_t MSG_LEN = 9;

  MH_Z19C();

  ~MH_Z19C() = default;

  MH_Z19C(const MH_Z19C&) = delete;
  MH_Z19C(MH_Z19C&&) = delete;
  MH_Z19C& operator=(const MH_Z19C&) = delete;
  MH_Z19C& operator=(MH_Z19C&&) = delete;

  py::str id() const;
  py::str type() const;
  py::str status() const;
  py::dict reading();

private:
  std::string m_id;
  int m_fd;
  std::array<byte, MSG_LEN> m_response_buffer;

};
