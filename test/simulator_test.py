import pytest
from gumnut_simulator.simulator import GumnutSimulator, SimulatorState



@pytest.fixture
def gsimulator():
    return GumnutSimulator()


def test_simulator_reset(gsimulator):
    gsimulator.reset()
    assert gsimulator.asm_source == ""
    assert gsimulator.number_of_instructions == 0

    assert gsimulator.get_state() == SimulatorState.halt
    assert gsimulator.get_breakpoints() == []
    assert gsimulator.get_current_line() == -1

    assert gsimulator.get_instruction_memory() == [0] * 4096
    assert gsimulator.get_data_memory() == [0] * 256
    assert gsimulator.get_flags() == {"CARRY": False, "ZERO": False, "WAIT": False, "STBY": False, "IREN": False }