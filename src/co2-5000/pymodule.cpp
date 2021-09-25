#include <pybind11/pybind11.h>

#include "driver.h"

namespace py = pybind11;


PYBIND11_MODULE(_co2_5000, m)
{
  m.doc() = "pybind11 bindings for MH-Z19C carbon dioxide sensor";

  py::class_<CO2_5000>(m, "Sensor")
    .def(py::init<>(), "construct")
    .def("id", &CO2_5000::id, "Get sensor id")
    .def("type", &CO2_5000::type, "Get sensor type")
    .def("status", &CO2_5000::status, "Get sensor status")
    .def("read", &CO2_5000::reading, "Read data from sensor");

  m.def("crc", [](py::bytes b) {
    py::buffer_info info(py::buffer(b).request());
    const uint8_t *data = reinterpret_cast<const uint8_t*>(info.ptr);
    if (info.ndim != 1)
      throw py::value_error("bytes must be 1d array");
    std::array<uint8_t, 2> crc = calc_crc(data, info.shape[0]);
    return py::bytes(std::string(crc.begin(), crc.end()));
  })
  .def("check_crc", [](py::bytes b) {
    py::buffer_info info(py::buffer(b).request());
    if (info.ndim != 1)
      throw py::value_error("bytes must be 1d array");
    const uint8_t *data = reinterpret_cast<const uint8_t*>(info.ptr);
    return check_crc(data, info.shape[0]);
  });
}

