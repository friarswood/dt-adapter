import os
from setuptools import find_packages, setup
from pybind11.setup_helpers import Pybind11Extension, ParallelCompile


def get_defines(env):
  if os.getenv(env):
    return[(env, "")]
  return None

def get_libs(env):
  libs = {
    "HAVE_PISENSEHAT": ["-lRTIMULib"],
    "HAVE_CO2_5000": ["-lwiringPi"]
  }
  if os.getenv(env):
    return libs.get(env)
  return None


ext_modules = [
  Pybind11Extension(
    '_pisensehat',
    sources=["src/pisensehat/pymodule.cpp", "src/pisensehat/pisensehat.cpp"],
    depends=["src/pisensehat/pisensehat.h", "src/pisensehat/RTIMULib_stub.h", "setup.py", "dt_adapter/__init__.py"],
    define_macros=get_defines("HAVE_PISENSEHAT"),
    extra_link_args=get_libs("HAVE_PISENSEHAT"),
    cxx_std=17
  ),
  Pybind11Extension(
    '_co2_5000',
    sources=["src/co2-5000/pymodule.cpp", "src/co2-5000/driver.cpp"],
    depends=["src/co2-5000/driver.h", "setup.py", "dt_adapter/__init__.py"],
    define_macros=get_defines("HAVE_CO2_5000"),
    extra_link_args=get_libs("HAVE_CO2_5000"),
    cxx_std=17
  )
]

ParallelCompile().install()

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
    'numpy',
    'python-dotenv',
  ],
  tests_require=["pytest"]
)
