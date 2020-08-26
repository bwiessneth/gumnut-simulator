import random
import pytest

from gumnut.GumnutCore import GumnutCore  # noqa: E402
from gumnut import GumnutExceptions  # noqa: E402
from gumnut.GumnutDecoder import INSTR


@pytest.fixture
def gcore():
    return GumnutCore()


def test_fetch_limits(gcore):
    gcore.PC = 0
    gcore.fetch()

    with pytest.raises(GumnutExceptions.InvalidPCValue):
        gcore.PC = -1
        gcore.fetch()

    gcore.PC = 4095
    gcore.fetch()

    with pytest.raises(GumnutExceptions.InvalidPCValue):
        gcore.PC = 4096
        gcore.fetch()


def test_update_PC(gcore):
    gcore.PC = 0
    gcore.update_PC()
    assert gcore.PC == 1
    gcore.update_PC()
    assert gcore.PC == 2
    gcore.update_PC()
    assert gcore.PC == 3


def test_update_PC_limits(gcore):
    gcore.PC = 4093
    gcore.update_PC()
    assert gcore.PC == 4094

    gcore.update_PC()
    assert gcore.PC == 4095

    with pytest.raises(GumnutExceptions.InvalidPCValue):
        gcore.update_PC()  # PC = 4096 --> Exception must be raised

    gcore.PC = -100
    with pytest.raises(GumnutExceptions.InvalidPCValue):
        gcore.update_PC()


def test_upload_instruction_memory(gcore):
    test_data = [int(1000 * random.random()) for i in range(4096)]
    gcore.upload_instruction_memory(test_data)


def test_upload_instruction_memory_size_exceeded(gcore):
    test_data = [int(1000 * random.random()) for i in range(4097)]
    with pytest.raises(GumnutExceptions.InstructionMemorySizeExceeded):
        gcore.upload_instruction_memory(test_data)


def test_upload_data_memory(gcore):
    test_data = [int(1000 * random.random()) for i in range(256)]
    gcore.upload_data_memory(test_data)


def test_upload_data_memory_size_exceeded(gcore):
    test_data = [int(1000 * random.random()) for i in range(257)]
    with pytest.raises(GumnutExceptions.DataMemorySizeExceeded):
        gcore.upload_data_memory(test_data)


def test_check_data_memory_access(gcore):
    gcore.check_data_memory_access(gcore.data_memory_size)


def test_check_data_memory_access_violation(gcore):
    with pytest.raises(GumnutExceptions.DataMemoryAccessViolation):
        gcore.check_data_memory_access(gcore.data_memory_size + 1)


def test_add_instruction(gcore):
    assert gcore.r[1] == 0
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = 1
    instr = INSTR("add", 0, 1, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + 1 = 2
    instr = INSTR("add", 0, 1, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 2
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + 254 = 256 -> CARRY & r1 = 0
    instr = INSTR("add", 0, 1, 1, 254, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 0
    assert gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + 2 = 2 -> CARRY == False
    instr = INSTR("add", 0, 1, 1, 2, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 2
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + r1 = 4 -> CARRY == False
    instr = INSTR("add", 0, 1, 1, 1, "register")
    gcore.execute(instr)
    assert gcore.r[1] == 4
    assert not gcore.CARRY
    assert not gcore.ZERO


def test_addc_instruction(gcore):
    # r1 = 1
    instr = INSTR("addc", 0, 1, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + 1 = 2
    instr = INSTR("addc", 0, 1, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 2
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + 254 = 256 -> CARRY & r1 = 0
    instr = INSTR("addc", 0, 1, 1, 254, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 0
    assert gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + 2 = 2 -> CARRY == False
    instr = INSTR("addc", 0, 1, 1, 2, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 3
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 + r1 = 6 -> CARRY == False
    instr = INSTR("addc", 0, 1, 1, 1, "register")
    gcore.execute(instr)
    assert gcore.r[1] == 6
    assert not gcore.CARRY
    assert not gcore.ZERO


def test_sub_instruction(gcore):
    # r1 = 1
    instr = INSTR("add", 0, 1, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 - 4 = -3 -> CARRY & r1 = 253
    instr = INSTR("sub", 0, 1, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 253
    assert gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 - 4 = 249 -> CARRY == False
    instr = INSTR("sub", 0, 1, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 249
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 - r1 = 0 -> CARRY == False
    instr = INSTR("sub", 0, 1, 1, 1, "register")
    gcore.execute(instr)
    assert gcore.r[1] == 0
    assert not gcore.CARRY
    assert gcore.ZERO


def test_subc_instruction(gcore):
    # r1 = 1
    instr = INSTR("add", 0, 1, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 - 4 = -3 -> CARRY & r1 = 253
    instr = INSTR("subc", 0, 1, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 253
    assert gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 - 4 = 249 -> CARRY == False
    instr = INSTR("subc", 0, 1, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[1] == 248
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r1 = r1 - r1 = 0 -> CARRY == False
    instr = INSTR("subc", 0, 1, 1, 1, "register")
    gcore.execute(instr)
    assert gcore.r[1] == 0
    assert not gcore.CARRY
    assert gcore.ZERO


def test_and_immediate_instruction(gcore):
    # r2 = r1(0) & 0
    gcore.r[1] = 0
    instr = INSTR("and", None, 2, 1, 0, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r2 = r1(0) & 1
    gcore.r[1] = 0
    instr = INSTR("and", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r2 = r1(1) & 0
    gcore.r[1] = 1
    instr = INSTR("and", None, 2, 1, 0, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r2 = r1(1) & 1
    gcore.r[1] = 1
    instr = INSTR("and", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO


def test_and_register_instruction(gcore):
    # r3 = r1(0) & r2(0)
    gcore.r[1] = 0
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("and", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r3 = r1(0) & r2(1)
    gcore.r[1] = 1
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("and", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r3 = r1(1) & r2(0)
    gcore.r[1] = 1
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("and", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r3 = r1(1) & r2(1)
    gcore.r[1] = 1
    gcore.r[2] = 1
    gcore.r[3] = 0
    instr = INSTR("and", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO


def test_or_immediate_instruction(gcore):
    # r2 = r1(0) | 0
    gcore.r[1] = 0
    gcore.r[2] = 0
    instr = INSTR("or", None, 2, 1, 0, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r2 = r1(0) | 1
    gcore.r[1] = 0
    gcore.r[2] = 0
    instr = INSTR("or", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r2 = r1(1) | 0
    gcore.r[1] = 1
    gcore.r[2] = 0
    instr = INSTR("or", None, 2, 1, 0, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r2 = r1(1) | 1
    gcore.r[1] = 1
    gcore.r[2] = 0
    instr = INSTR("or", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO


def test_or_register_instruction(gcore):
    # r3 = r1(0) | r2(0)
    gcore.r[1] = 0
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("or", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r3 = r1(0) | r2(0)
    gcore.r[1] = 1
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("or", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r3 = r1(0) | r2(0)
    gcore.r[1] = 0
    gcore.r[2] = 1
    gcore.r[3] = 0
    instr = INSTR("or", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r3 = r1(0) | r2(0)
    gcore.r[1] = 1
    gcore.r[2] = 1
    gcore.r[3] = 0
    instr = INSTR("or", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO


def test_xor_immediate_instruction(gcore):
    # r2 = r1(0) XOR 0
    gcore.r[1] = 0
    gcore.r[2] = 0
    instr = INSTR("xor", None, 2, 1, 0, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r2 = r1(0) XOR 1
    gcore.r[1] = 0
    gcore.r[2] = 0
    instr = INSTR("xor", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r2 = r1(1) XOR 0
    gcore.r[1] = 1
    gcore.r[2] = 0
    instr = INSTR("xor", None, 2, 1, 0, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r2 = r1(1) XOR 1
    gcore.r[1] = 1
    gcore.r[2] = 0
    instr = INSTR("xor", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
    assert not gcore.CARRY
    assert gcore.ZERO


def test_xor_register_instruction(gcore):
    # r3 = r1(0) XOR r2(0)
    gcore.r[1] = 0
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("xor", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0
    assert not gcore.CARRY
    assert gcore.ZERO

    # r3 = r1(0) XOR r2(1)
    gcore.r[1] = 0
    gcore.r[2] = 1
    gcore.r[3] = 0
    instr = INSTR("xor", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r3 = r1(1) XOR r2(0)
    gcore.r[1] = 1
    gcore.r[2] = 0
    gcore.r[3] = 0
    instr = INSTR("xor", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 1
    assert not gcore.CARRY
    assert not gcore.ZERO

    # r3 = r1(1) XOR r2(1)
    gcore.r[1] = 1
    gcore.r[2] = 1
    gcore.r[3] = 0
    instr = INSTR("xor", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0
    assert not gcore.CARRY
    assert gcore.ZERO


def test_shl_instruction(gcore):
    # r2 = r1(1) << 1
    gcore.r[1] = 1
    gcore.r[2] = 0
    instr = INSTR("shl", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 2

    instr = INSTR("shl", None, 2, 1, 2, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 4

    instr = INSTR("shl", None, 2, 1, 3, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 8

    instr = INSTR("shl", None, 2, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 16

    instr = INSTR("shl", None, 2, 1, 5, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 32

    instr = INSTR("shl", None, 2, 1, 6, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 64

    instr = INSTR("shl", None, 2, 1, 7, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 128

    instr = INSTR("shl", None, 2, 1, 8, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0

    instr = INSTR("shl", None, 2, 1, 9, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0


def test_shr_instruction(gcore):
    # r2 = r1(128) >> 1
    gcore.r[1] = 128
    gcore.r[2] = 0
    instr = INSTR("shr", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 64

    instr = INSTR("shr", None, 2, 1, 2, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 32

    instr = INSTR("shr", None, 2, 1, 3, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 16

    instr = INSTR("shr", None, 2, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 8

    instr = INSTR("shr", None, 2, 1, 5, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 4

    instr = INSTR("shr", None, 2, 1, 6, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 2

    instr = INSTR("shr", None, 2, 1, 7, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1

    instr = INSTR("shr", None, 2, 1, 8, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0

    instr = INSTR("shr", None, 2, 1, 9, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0


def test_rol_instruction(gcore):
    pass
    return
    gcore.r[1] = 1
    gcore.r[2] = 0
    instr = INSTR("rol", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 2

    instr = INSTR("rol", None, 2, 1, 2, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 4

    instr = INSTR("rol", None, 2, 1, 3, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 8

    instr = INSTR("rol", None, 2, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 16

    instr = INSTR("rol", None, 2, 1, 5, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 32

    instr = INSTR("rol", None, 2, 1, 6, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 64

    instr = INSTR("rol", None, 2, 1, 7, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 128

    instr = INSTR("rol", None, 2, 1, 8, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1

    instr = INSTR("rol", None, 2, 1, 9, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 2


def test_ror_instruction(gcore):
    pass
    return
    gcore.r[1] = 128
    gcore.r[2] = 0
    instr = INSTR("ror", None, 2, 1, 1, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 64

    instr = INSTR("ror", None, 2, 1, 2, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 32

    instr = INSTR("ror", None, 2, 1, 3, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 16

    instr = INSTR("ror", None, 2, 1, 4, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 8

    instr = INSTR("ror", None, 2, 1, 5, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 4

    instr = INSTR("ror", None, 2, 1, 6, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 2

    instr = INSTR("ror", None, 2, 1, 7, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 1

    instr = INSTR("ror", None, 2, 1, 8, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0

    instr = INSTR("ror", None, 2, 1, 9, "immediate")
    gcore.execute(instr)
    assert gcore.r[2] == 0
