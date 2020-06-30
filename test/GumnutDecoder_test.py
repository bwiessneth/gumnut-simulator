__author__ = "BW"

# Add current directory to PYTHONPATH
import os, sys

sys.path.insert(0, os.getcwd())
# print('sys.path = ', sys.path)


from GumnutSimulator import GumnutDecoder


def test_decode_arithmetic_instructions():
    dec = GumnutDecoder.GumnutDecoder()

    # Arithmetic/Logic
    # register access
    assert dec.decode_instruction(0x38A60) == GumnutDecoder.INSTR("add", 0, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A61) == GumnutDecoder.INSTR("addc", 1, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A62) == GumnutDecoder.INSTR("sub", 2, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A63) == GumnutDecoder.INSTR("subc", 3, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A64) == GumnutDecoder.INSTR("and", 4, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A65) == GumnutDecoder.INSTR("or", 5, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A66) == GumnutDecoder.INSTR("xor", 6, 1, 2, 3, "register")
    assert dec.decode_instruction(0x38A67) == GumnutDecoder.INSTR("mask", 7, 1, 2, 3, "register")
    # add r8, r9, r10 will cause an jmp to 0x2368
    # assert dec.decode_instruction(248128) == GumnutDecoder.INSTR('add', 0, 8, 9, 10, 'register')

    # immediate access
    assert dec.decode_instruction(0x0) == GumnutDecoder.INSTR("add", 0, 0, 0, 0, "immediate")
    assert dec.decode_instruction(0xA12) == GumnutDecoder.INSTR("add", 0, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0x4A12) == GumnutDecoder.INSTR("addc", 1, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0x8A12) == GumnutDecoder.INSTR("sub", 2, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0xCA12) == GumnutDecoder.INSTR("subc", 3, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0x10A12) == GumnutDecoder.INSTR("and", 4, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0x14A12) == GumnutDecoder.INSTR("or", 5, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0x18A12) == GumnutDecoder.INSTR("xor", 6, 1, 2, 18, "immediate")
    assert dec.decode_instruction(0x1CA12) == GumnutDecoder.INSTR("mask", 7, 1, 2, 18, "immediate")


def test_decode_shift_instructions():
    dec = GumnutDecoder.GumnutDecoder()

    # Shift instructions
    assert dec.decode_instruction(0x30000) == GumnutDecoder.INSTR("shl", 0, 0, 0, 0, None)
    assert dec.decode_instruction(0x30A80) == GumnutDecoder.INSTR("shl", 0, 1, 2, 4, None)
    assert dec.decode_instruction(0x30A81) == GumnutDecoder.INSTR("shr", 1, 1, 2, 4, None)
    assert dec.decode_instruction(0x30A82) == GumnutDecoder.INSTR("rol", 2, 1, 2, 4, None)
    assert dec.decode_instruction(0x30A83) == GumnutDecoder.INSTR("ror", 3, 1, 2, 4, None)


def test_decode_memory_io_instructions():
    dec = GumnutDecoder.GumnutDecoder()

    # Memory and I/O instructions
    # Direct offset
    assert dec.decode_instruction(0x20812) == GumnutDecoder.INSTR("ldm", 0, 1, 0, 18, None)
    assert dec.decode_instruction(0x24812) == GumnutDecoder.INSTR("stm", 1, 1, 0, 18, None)
    assert dec.decode_instruction(0x28812) == GumnutDecoder.INSTR("inp", 2, 1, 0, 18, None)
    assert dec.decode_instruction(0x2C812) == GumnutDecoder.INSTR("out", 3, 1, 0, 18, None)
    # Register + offset
    assert dec.decode_instruction(0x20A12) == GumnutDecoder.INSTR("ldm", 0, 1, 2, 18, None)
    assert dec.decode_instruction(0x24A12) == GumnutDecoder.INSTR("stm", 1, 1, 2, 18, None)
    assert dec.decode_instruction(0x28A12) == GumnutDecoder.INSTR("inp", 2, 1, 2, 18, None)
    assert dec.decode_instruction(0x2CA12) == GumnutDecoder.INSTR("out", 3, 1, 2, 18, None)


def test_decode_branch_instructions():
    dec = GumnutDecoder.GumnutDecoder()

    # Branch instructions
    assert dec.decode_instruction(0x3E0FF) == GumnutDecoder.INSTR("bz", 0, 0, 0, 255, None)
    assert dec.decode_instruction(0x3E000) == GumnutDecoder.INSTR("bz", 0, 0, 0, 0, None)
    assert dec.decode_instruction(0x3E080) == GumnutDecoder.INSTR("bz", 0, 0, 0, 128, None)
    assert dec.decode_instruction(0x3E4FF) == GumnutDecoder.INSTR("bnz", 1, 0, 0, 255, None)
    assert dec.decode_instruction(0x3E400) == GumnutDecoder.INSTR("bnz", 1, 0, 0, 0, None)
    assert dec.decode_instruction(0x3E47F) == GumnutDecoder.INSTR("bnz", 1, 0, 0, 127, None)
    assert dec.decode_instruction(0x3E8FF) == GumnutDecoder.INSTR("bc", 2, 0, 0, 255, None)
    assert dec.decode_instruction(0x3E800) == GumnutDecoder.INSTR("bc", 2, 0, 0, 0, None)
    assert dec.decode_instruction(0x3E87F) == GumnutDecoder.INSTR("bc", 2, 0, 0, 127, None)
    assert dec.decode_instruction(0x3ECFF) == GumnutDecoder.INSTR("bnc", 3, 0, 0, 255, None)
    assert dec.decode_instruction(0x3EC00) == GumnutDecoder.INSTR("bnc", 3, 0, 0, 0, None)
    assert dec.decode_instruction(0x3EC7F) == GumnutDecoder.INSTR("bnc", 3, 0, 0, 127, None)


def test_decode_jump_instructions():
    dec = GumnutDecoder.GumnutDecoder()

    # Jump instructions
    assert dec.decode_instruction(0x3C000) == GumnutDecoder.INSTR("jmp", 0, 0, 0, 0, None)
    assert dec.decode_instruction(0x3CFFF) == GumnutDecoder.INSTR("jmp", 0, 0, 0, 4095, None)
    assert dec.decode_instruction(0x3D000) == GumnutDecoder.INSTR("jsb", 1, 0, 0, 0, None)
    assert dec.decode_instruction(0x3DFFF) == GumnutDecoder.INSTR("jsb", 1, 0, 0, 4095, None)


def test_decode_misc_instructions():
    dec = GumnutDecoder.GumnutDecoder()

    # Misc instructions
    assert dec.decode_instruction(0x3F000) == GumnutDecoder.INSTR("ret", 0, 0, 0, 0, None)
    assert dec.decode_instruction(0x3F100) == GumnutDecoder.INSTR("reti", 1, 0, 0, 0, None)
    assert dec.decode_instruction(0x3F200) == GumnutDecoder.INSTR("enai", 2, 0, 0, 0, None)
    assert dec.decode_instruction(0x3F300) == GumnutDecoder.INSTR("disi", 3, 0, 0, 0, None)
    assert dec.decode_instruction(0x3F400) == GumnutDecoder.INSTR("wait", 4, 0, 0, 0, None)
    assert dec.decode_instruction(0x3F500) == GumnutDecoder.INSTR("stby", 5, 0, 0, 0, None)
