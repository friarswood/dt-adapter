#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

using namespace py::literals;
using namespace std::string_literals;


py::dict read_sensor() 
{
  py::dict result;
  result["temperature"] = 20.0;
  result["humidity"] = 0.5;
  result["pressure"] = 1000.0;

  return result;
}

PYBIND11_MODULE(pisensehat, m) 
{
  m.doc() = "pybind11 bindings for Pi sense hat";

  m.def("read", &read_sensor, "Read sensor");
}

