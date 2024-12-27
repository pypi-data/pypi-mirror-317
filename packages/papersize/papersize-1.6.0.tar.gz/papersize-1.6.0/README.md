# papersize 📏 Paper size related tools

This module provides tools to manipulate paper sizes, that is:

- a dictionary of several named standard names (e.g. A4, letter) , with their respective sizes (width and height);
- functions to convert sizes from one unit (e.g. inches) to another (e.g. centimeters);
- functions to manipulate paper orientation (portrait or landscape);
- tools to parse paper sizes, so that you do not have to worry about the format of paper sizes provided by your user, it being `"a4"` or `"21cm x 29.7cm"`.

## What's new?

See [changelog](https://git.framasoft.org/spalax/papersize/blob/main/CHANGELOG.md>).

## Install

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/papersize
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system):

        python3 -m pip install .

* From pip:

      pip install papersize

## Test

* Current python version:

      python3 -m unittest

* All supported python versions (using [tox](http://tox.testrun.org)):

      tox

## Documentation

The documentation is available on [readthedocs](http://papersize.readthedocs.io).  You can build it using:

    cd doc && make html
