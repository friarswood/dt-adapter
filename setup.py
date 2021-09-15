import os
from setuptools import find_packages, setup
from pybind11.setup_helpers import Pybind11Extension


def get_defines():
  if os.getenv("SENSOR_STUB"):
    return [("SENSOR_STUB", "")]
  return None


def get_libs():
  if os.getenv("SENSOR_STUB"):
    return None
  return ['-lRTIMULib']


ext_modules = [
  Pybind11Extension(
    '_pisensehat',
    sources=["src/pymodule.cpp", "src/pisensehat.cpp"],
    depends=["src/pisensehat.h", "setup.py", "dt_adapter/__init__.py"],
    define_macros=get_defines(),
    extra_link_args=get_libs(),
    cxx_std=17
  )
]

setup(
  name='dt_adapter',
  packages=find_packages(),
  ext_modules=ext_modules,
  scripts=[
    "transmit.py"
  ],
  include_package_data=True,
  zip_safe=False,
  setup_requires=['pybind11>=2.6.0', 'pytest-runner', 'wheel'],
  install_requires=[
    'requests',
    'pyjwt',
    'python-dotenv',
  ],
  tests_require=["pytest"]
)
