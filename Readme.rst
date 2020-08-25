Gumnut Simulator
================

This projects contains several components which all revolve around Peter Ashenden's 8-bit soft-core
called *Gumnut*. For more information refer to *The Designers Guide to VHDL*
https://www.sciencedirect.com/book/9780120887859/the-designers-guide-to-vhdl

This repository was forked from my very first implementation created at the laboratory for digital
engineering at the University of Applied Sciences Augsburg back in 2015.



GumnutCore
----------



GumnutDecoder
-------------



GumnutExceptions
----------------



Documentation
=============

Please refer to https://example.com



Development
===========

Setup
-----

Virtual environment
~~~~~~~~~~~~~~~~~~~

You definitely want to create an isolated python environment for development. That way the required
packages you are going to install with ``pip`` are encapsulated form your systemwide python
installation. For more info check https://virtualenv.pypa.io/en/latest/

::

  [john@desktop ~]$ cd gumnut-simulator
  [john@desktop gumnut-simulator]$ virtualenv ENV -p python3

You can activate your new python environment like this:

::

  [john@desktop gumnut-simulator]$ source ENV/bin/activate
  (ENV) [john@desktop gumnut-simulator]$

Once you're done playing with it, deactivate it with the following command:

::

  (ENV) [john@desktop gumnut-simulator]$ deactivate
  [john@desktop gumnut-simulator]$


Development dependecies
~~~~~~~~~~~~~~~~~~~~~~~

Activate the virtual environment and install the package via ``pip`` in editing-mode with the
development dependencies:

::

  (ENV) [john@desktop gumnut-simulator]$ pip install -e .[dev]

