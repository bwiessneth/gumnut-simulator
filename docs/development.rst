Development
###########

On this page you can find some pointers and remarks regarding development for this project.



Virtual environment
*******************

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
************************

Activate the virtual environment and install the package via ``pip`` in editing-mode with the
development dependencies:

::

  (ENV) [ziggy@stardust gumnut-simulator]$ pip install -e .[dev]



Tools
*****

This project comes with a few tools pre-configured. Refer to the following sections on how to use them.



tox
===

	Command line driven CI frontend and development task automation tool

For more info check https://tox.readthedocs.io/en/latest/

See ``tox.ini`` for:

* various tool options/overrides for various tools like ``flake8`` or ``black``
* definitions of test environments which are used
* various helper commands like ``build``, ``docs``, or ``publish``



pytest
======

	helps you write better programs

For more info check https://docs.pytest.org/en/stable/

The tests are located within the ``test`` directory. 
``pytest`` will look for them in that directory and run them.
To run the tests simply call ``tox -e pytest`` from the project root with the virtual environment enabled.



black
=====

	The uncompromising code formatter

For more info check https://black.readthedocs.io/en/stable/

Run it via calling ``tox -e pytest`` from the project root with the virtual environment enabled.



flake8
======

	Flake8: Your Tool For Style Guide Enforcement

For more info check https://flake8.pycqa.org/en/latest/

Run it via calling ``tox -e flake8`` from the project root with the virtual environment enabled.



pylint
======

	Pylint is a Python static code analysis tool which looks for programming
	errors, helps enforcing a coding standard, sniffs for code smells and offers
	simple refactoring suggestions.

For more info check http://pylint.pycqa.org/en/latest/

Run it via calling ``tox -e pylint`` from the project root with the virtual environment enabled.



TODO: docs
==========

```sphinx`` is used for documentation generation.

For more info check https://www.sphinx-doc.org/en/master/index.html

Run it via calling ``tox -e docs`` from the project root with the virtual environment enabled.



TODO: build
===========



TODO: publish
=============



Config files
************

pyproject.toml
==============

Set the default line width which is used by ``black``.



pylintrc
========

Inject virtual env path so that ``pylint`` can find the right packages when invoced by ``tox -e pylint``.



Tests
*****

``pytest`` and ``tox``  are used for testing. The tests and the needed files are located within the ``test`` directory. 
To run the tests simply call ``tox -e pytest`` from the project root with the virtual environment enabled.
``tox`` will take care of installing the *gumnut-simulator* package in development mode and run the tests against it.



Scope of tests
==============

Tests are run against:

* the *gumnut-simulator* package (this way also the code-coverage is determined)



Packaging for PyPI
******************

To package the project for distribution and publishing it on PyPI a few steps are involved.
For more information see https://packaging.python.org/tutorials/packaging-projects/

* Set version in ``gumnut-simulator\__init__.py``
* Run ``tox -e build``
* Run ``tox -e publish-test``
* Download and install from test index ``python -m pip install --index-url https://test.pypi.org/simple/ --no-deps gumnut-simulator``

If all seems alright, repeat above steps and upload to the real PyPI.

* Run ``tox -e publish``
* Download and install from live index ``python -m pip install gumnut-simulator``
