
#include "sensor.h"
#include "timestamp.h"

class PySensor : public Sensor
{
public:
	//using Abstract::Abstract;

	py::str type() const override
  {
		PYBIND11_OVERLOAD_PURE(py::str, Sensor, type);
	}

	py::str id() const override
  {
		PYBIND11_OVERLOAD_PURE(py::str, Sensor, id);
	}

	py::str status() const override
  {
		PYBIND11_OVERLOAD_PURE(py::str, Sensor, type);
	}

	py::dict read() override
  {
		PYBIND11_OVERLOAD_PURE(py::dict, Sensor, read);
	}
};

PYBIND11_MODULE(_common, m)
{
	py::class_<Sensor, PySensor>(m, "Sensor")
    .def(py::init<>())
    .def("type", &Sensor::type)
    .def("id", &Sensor::id)
    .def("", &Sensor::status)
    .def("read", &Sensor::read);

	m.def("utc_now", &utc_now);
}

