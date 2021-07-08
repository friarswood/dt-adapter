#include <pybind11/pybind11.h>

#include "pisensehat.h"

namespace py = pybind11;


PYBIND11_MODULE(_pisensehat, m)
{
  m.doc() = "pybind11 bindings for Pi sense hat";

  py::class_<PiSenseHat>(m, "PiSenseHat")
    .def(py::init<>(), "construct")
    .def("status", &PiSenseHat::status, "Get sensor status")
    .def("read", &PiSenseHat::read, "Read data from sensor");
}

