from setuptools import setup, find_packages
import functools
import os
import sys

_PYTHON_VERSION = sys.version_info
_IS_PYPY = hasattr(sys, 'pypy_version_info')
_in_same_dir = functools.partial(os.path.join, os.path.dirname(__file__))

with open(_in_same_dir("butler", "__version__.py")) as version_file:
    exec(version_file.read())  # pylint: disable=W0122

install_requires = [
    "Flask",
    "requests>=1.1.0",
]


setup(name="butler",
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ],
      description="Light flask server",
      license="BSD",
      author="Eli Plaut",
      author_email="eplaut@gmail.com",
      url="http://butler.github.com/",
      version=__version__,  # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),
      install_requires=install_requires,
)
