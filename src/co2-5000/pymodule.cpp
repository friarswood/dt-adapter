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
}

