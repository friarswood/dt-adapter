#include <pybind11/pybind11.h>

#include "mh-z19c.h"

namespace py = pybind11;


PYBIND11_MODULE(_mh_z19c, m)
{
  m.doc() = "pybind11 bindings for MH-Z19C carbon dioxide sensor";

  py::class_<MH_Z19C>(m, "Sensor")
    .def(py::init<>(), "construct")
    .def("id", &MH_Z19C::id, "Get sensor id")
    .def("type", &MH_Z19C::type, "Get sensor type")
    .def("status", &MH_Z19C::status, "Get sensor status")
    .def("read", &MH_Z19C::reading, "Read data from sensor");
}

