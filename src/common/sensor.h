#pragma once

#include <pybind11/pybind11.h>

namespace py = pybind11;

// Interface for sensor drivers
class Sensor
{
public:

  virtual ~Sensor() { };

  virtual py::str id() const = 0;

  virtual py::str type() const = 0;

  virtual py::str status() const = 0;

  virtual py::dict read() const = 0;

};

