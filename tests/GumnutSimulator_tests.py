__author__ = 'BW'

# Add current directory to PYTHONPATH
import os, sys
sys.path.insert(0, os.getcwd())
#print('sys.path = ', sys.path)


from nose.tools import *
from GumnutSimulator import GumnutSimulator

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_basic():
    mySim = GumnutSimulator.GumnutSimulator()
    print("I RAN!")
