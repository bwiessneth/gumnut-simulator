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

  [ziggy@stardust ~]$ cd gumnut-simulator
  [ziggy@stardust gumnut-simulator]$ virtualenv ENV -p python3

You can activate your new python environment like this:

::

  [ziggy@stardust gumnut-simulator]$ source ENV/bin/activate
  (ENV) [ziggy@stardust gumnut-simulator]$

Once you're done playing with it, deactivate it with the following command:

::

  (ENV) [ziggy@stardust gumnut-simulator]$ deactivate
  [ziggy@stardust gumnut-simulator]$


Development dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

Activate the virtual environment and install the package via ``pip`` in editing-mode with the
development dependencies:

::

  (ENV) [ziggy@stardust gumnut-simulator]$ pip install -e .[dev]



Tools
-----

This project comes with a few tools pre-configured. Refer to the following sections on how to use them.



tox
~~~

	Command line driven CI frontend and development task automation tool

For more info check https://tox.readthedocs.io/en/latest/

See ``tox.ini`` for:

* various tool options/overrides for various tools like ``flake8`` or ``black``
* definitions of test environments which are used
* various helper commands like ``build``, ``docs``, or ``publish``



pytest
~~~~~~

	helps you write better programs

For more info check https://docs.pytest.org/en/stable/

The tests are located within the ``test`` directory. 
``pytest`` will look for them in that directory and run them.
To run the tests simply call ``tox -e pytest`` from the project root with the virtual environment enabled.



black
~~~~~

	The uncompromising code formatter

For more info check https://black.readthedocs.io/en/stable/

Run it via calling ``tox -e pytest`` from the project root with the virtual environment enabled.



flake8
~~~~~~

	Flake8: Your Tool For Style Guide Enforcement

For more info check https://flake8.pycqa.org/en/latest/

Run it via calling ``tox -e flake8`` from the project root with the virtual environment enabled.



pylint
~~~~~~

	Pylint is a Python static code analysis tool which looks for programming
	errors, helps enforcing a coding standard, sniffs for code smells and offers
	simple refactoring suggestions.

For more info check http://pylint.pycqa.org/en/latest/

Run it via calling ``tox -e pylint`` from the project root with the virtual environment enabled.



TODO: docs
~~~~~~~~~~

```sphinx`` is used for documentation generation.

For more info check https://www.sphinx-doc.org/en/master/index.html

Run it via calling ``tox -e docs`` from the project root with the virtual environment enabled.



TODO: build
~~~~~~~~~~~



TODO: publish
~~~~~~~~~~~~~
