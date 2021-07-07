from setuptools import find_packages, setup
from pybind11.setup_helpers import Pybind11Extension
from setuptools.command.build_ext import build_ext
import subprocess

ext_modules = [
  Pybind11Extension(
    'pisensehat',
    sources=["src/pymodule.cpp", "src/sensors.cpp"],
    depends=["setup.py", "dt_adapter/__init__.py"],
    #include_dirs=["src/ei"],
    extra_link_args = ['-lRTIMULib'],
    cxx_std=17
  )
]

setup(
  name='dt_adapter',
  packages=find_packages(),
  #cmdclass={"build_ext": BuildEiLib}, #, 'build_py': ext_modules[0]},
  ext_modules=ext_modules,
  scripts=[
  ],
  include_package_data=True,
  zip_safe=False,
  setup_requires=['pybind11>=2.6.0', 'pytest-runner', 'wheel'],
  install_requires=[
    'requests',
    'disruptive',
    'python-dotenv',
  ],
  tests_require=["pytest"]
)

