__author__ = "BW"

# Add current directory to PYTHONPATH
import os
import sys

sys.path.insert(0, os.getcwd())


def setup():
    print("SETUP!")


def teardown():
    print("TEAR DOWN!")


def test_basic():
    print("I RAN!")
