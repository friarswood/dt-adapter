#include <pybind11/pybind11.h>

#include "pisensehat.h"

namespace py = pybind11;


PYBIND11_MODULE(_pisensehat, m)
{
  m.doc() = "pybind11 bindings for Pi sense hat (LSM9DS1)";

  py::class_<PiSenseHat>(m, "PiSenseHat")
    .def(py::init<>(), "construct")
    // calls back to python for the MTU ID
    .def_static("id", [](){ return py::module::import("dt_adapter").attr("get_device_id")(); }, "Get sensor id")
    .def("type", &PiSenseHat::type, "Get sensor type")
    .def("status", &PiSenseHat::status, "Get sensor status")
    .def("read", &PiSenseHat::read, "Read data from sensor");
}

