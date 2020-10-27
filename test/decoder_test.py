import pytest
from gumnut_simulator.decoder import GumnutDecoder, INSTR


@pytest.fixture
def gdecoder():
    return GumnutDecoder()


def test_decode_arithmetic_instructions(gdecoder):

    # Arithmetic/Logic
    # register access
    assert gdecoder.decode_instruction(0x38A60) == INSTR("add", 0, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A61) == INSTR("addc", 1, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A62) == INSTR("sub", 2, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A63) == INSTR("subc", 3, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A64) == INSTR("and", 4, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A65) == INSTR("or", 5, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A66) == INSTR("xor", 6, 1, 2, 3, "register")
    assert gdecoder.decode_instruction(0x38A67) == INSTR("mask", 7, 1, 2, 3, "register")
    # add r8, r9, r10 will cause an jmp to 0x2368
    # assert gdecoder.decode_instruction(248128) == INSTR('add', 0, 8, 9, 10, 'register')

    # immediate access
    assert gdecoder.decode_instruction(0x0) == INSTR("add", 0, 0, 0, 0, "immediate")
    assert gdecoder.decode_instruction(0xA12) == INSTR("add", 0, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0x4A12) == INSTR("addc", 1, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0x8A12) == INSTR("sub", 2, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0xCA12) == INSTR("subc", 3, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0x10A12) == INSTR("and", 4, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0x14A12) == INSTR("or", 5, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0x18A12) == INSTR("xor", 6, 1, 2, 18, "immediate")
    assert gdecoder.decode_instruction(0x1CA12) == INSTR("mask", 7, 1, 2, 18, "immediate")


def test_decode_shift_instructions(gdecoder):

    # Shift instructions
    assert gdecoder.decode_instruction(0x30000) == INSTR("shl", 0, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x30A80) == INSTR("shl", 0, 1, 2, 4, None)
    assert gdecoder.decode_instruction(0x30A81) == INSTR("shr", 1, 1, 2, 4, None)
    assert gdecoder.decode_instruction(0x30A82) == INSTR("rol", 2, 1, 2, 4, None)
    assert gdecoder.decode_instruction(0x30A83) == INSTR("ror", 3, 1, 2, 4, None)


def test_decode_memory_io_instructions(gdecoder):

    # Memory and I/O instructions
    # Direct offset
    assert gdecoder.decode_instruction(0x20812) == INSTR("ldm", 0, 1, 0, 18, None)
    assert gdecoder.decode_instruction(0x24812) == INSTR("stm", 1, 1, 0, 18, None)
    assert gdecoder.decode_instruction(0x28812) == INSTR("inp", 2, 1, 0, 18, None)
    assert gdecoder.decode_instruction(0x2C812) == INSTR("out", 3, 1, 0, 18, None)
    # Register + offset
    assert gdecoder.decode_instruction(0x20A12) == INSTR("ldm", 0, 1, 2, 18, None)
    assert gdecoder.decode_instruction(0x24A12) == INSTR("stm", 1, 1, 2, 18, None)
    assert gdecoder.decode_instruction(0x28A12) == INSTR("inp", 2, 1, 2, 18, None)
    assert gdecoder.decode_instruction(0x2CA12) == INSTR("out", 3, 1, 2, 18, None)


def test_decode_branch_instructions(gdecoder):

    # Branch instructions
    assert gdecoder.decode_instruction(0x3E0FF) == INSTR("bz", 0, 0, 0, 255, None)
    assert gdecoder.decode_instruction(0x3E000) == INSTR("bz", 0, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3E080) == INSTR("bz", 0, 0, 0, 128, None)
    assert gdecoder.decode_instruction(0x3E4FF) == INSTR("bnz", 1, 0, 0, 255, None)
    assert gdecoder.decode_instruction(0x3E400) == INSTR("bnz", 1, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3E47F) == INSTR("bnz", 1, 0, 0, 127, None)
    assert gdecoder.decode_instruction(0x3E8FF) == INSTR("bc", 2, 0, 0, 255, None)
    assert gdecoder.decode_instruction(0x3E800) == INSTR("bc", 2, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3E87F) == INSTR("bc", 2, 0, 0, 127, None)
    assert gdecoder.decode_instruction(0x3ECFF) == INSTR("bnc", 3, 0, 0, 255, None)
    assert gdecoder.decode_instruction(0x3EC00) == INSTR("bnc", 3, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3EC7F) == INSTR("bnc", 3, 0, 0, 127, None)


def test_decode_jump_instructions(gdecoder):

    # Jump instructions
    assert gdecoder.decode_instruction(0x3C000) == INSTR("jmp", 0, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3CFFF) == INSTR("jmp", 0, 0, 0, 4095, None)
    assert gdecoder.decode_instruction(0x3D000) == INSTR("jsb", 1, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3DFFF) == INSTR("jsb", 1, 0, 0, 4095, None)


def test_decode_misc_instructions(gdecoder):

    # Misc instructions
    assert gdecoder.decode_instruction(0x3F000) == INSTR("ret", 0, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3F100) == INSTR("reti", 1, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3F200) == INSTR("enai", 2, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3F300) == INSTR("disi", 3, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3F400) == INSTR("wait", 4, 0, 0, 0, None)
    assert gdecoder.decode_instruction(0x3F500) == INSTR("stby", 5, 0, 0, 0, None)
