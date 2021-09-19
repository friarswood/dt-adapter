#include <pybind11/pybind11.h>

#include "pisensehat.h"

namespace py = pybind11;


PYBIND11_MODULE(_pisensehat, m)
{
  m.doc() = "pybind11 bindings for Pi sense hat (LSM9DS1)";

  py::class_<PiSenseHat>(m, "Sensor")
    .def(py::init<>(), "construct")
    .def("id", &PiSenseHat::id, "Get sensor id")
    .def("type", &PiSenseHat::type, "Get sensor type")
    .def("status", &PiSenseHat::status, "Get sensor status")
    .def("read", &PiSenseHat::read, "Read data from sensor");
}

