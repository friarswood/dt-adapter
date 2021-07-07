#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "sensors.h"

namespace py = pybind11;

using namespace py::literals;
using namespace std::string_literals;


py::dict read_sensor() 
{
  py::dict result;

  double t, p, h;
  std::string timestamp;
    
  Sensors::Status::value status = Global::instance<Sensors>().get(timestamp, t, p, h);

  result["status"] = Sensors::statusToString(status);
  result["time"] = timestamp;

  if (status != Sensors::Status::NO_IMU)
  {
    result["temperature"] = t;
    if (!(status & Sensors::Status::NO_PRESSURE))
    {
      result["temperature"] = t;
      result["pressure"] = p;
    }
    if (!(status & Sensors::Status::NO_HUMIDITY))
    {
      result["humidity"] = h;
    }
  }

  return result;
}

PYBIND11_MODULE(pisensehat, m) 
{
  m.doc() = "pybind11 bindings for Pi sense hat";

  m.def("read", &read_sensor, "Read sensor");
}

