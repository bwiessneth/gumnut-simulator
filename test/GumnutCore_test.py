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

    with pytest.raises(GumnutExceptions.InvalidPCValue) as e:
        gcore.PC = -1
        gcore.fetch()
    print(e.__repr__())
    print(e.value.as_dict())

    gcore.PC = 4095
    gcore.fetch()

    with pytest.raises(GumnutExceptions.InvalidPCValue) as e:
        gcore.PC = 4096
        gcore.fetch()
    print(e.__repr__())
    print(e.value.as_dict())


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

    with pytest.raises(GumnutExceptions.InvalidPCValue) as e:
        gcore.update_PC()  # PC = 4096 --> Exception must be raised
    print(e.__repr__())
    print(e.value.as_dict())

    gcore.PC = -100
    with pytest.raises(GumnutExceptions.InvalidPCValue) as e:
        gcore.update_PC()
    print(e.__repr__())
    print(e.value.as_dict())


def test_upload_instruction_memory(gcore):
    test_data = [int(1000 * random.random()) for i in range(4096)]
    gcore.upload_instruction_memory(test_data)


def test_upload_instruction_memory_size_exceeded(gcore):
    test_data = [int(1000 * random.random()) for i in range(4097)]
    with pytest.raises(GumnutExceptions.InstructionMemorySizeExceeded) as e:
        gcore.upload_instruction_memory(test_data)
    print(e.__repr__())
    print(e.value.as_dict())


def test_upload_data_memory(gcore):
    test_data = [int(1000 * random.random()) for i in range(256)]
    gcore.upload_data_memory(test_data)


def test_upload_data_memory_size_exceeded(gcore):
    test_data = [int(1000 * random.random()) for i in range(257)]
    with pytest.raises(GumnutExceptions.DataMemorySizeExceeded) as e:
        gcore.upload_data_memory(test_data)
    print(e.__repr__())
    print(e.value.as_dict())


def test_check_data_memory_access(gcore):
    gcore.check_data_memory_access(gcore.data_memory_size)


def test_check_data_memory_access_violation(gcore):
    with pytest.raises(GumnutExceptions.DataMemoryAccessViolation) as e:
        gcore.check_data_memory_access(gcore.data_memory_size + 1)
    print(e.__repr__())
    print(e.value.as_dict())


def test_step(gcore):
    # TODO: Extend test a bit. Currently only checking that there's no exception!
    gcore.step()


def test_unknown_instruction(gcore):
    instr = INSTR("todo", 0, 1, 1, 1, "immediate")
    with pytest.raises(GumnutExceptions.InvalidInstruction) as e:
        gcore.execute(instr)
    print(e.__repr__())
    print(e.value.as_dict())


def test_empty_instruction(gcore):
    instr = None
    with pytest.raises(GumnutExceptions.InvalidInstruction) as e:
        gcore.execute(instr)
    print(e.__repr__())
    print(e.value.as_dict())


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


def test_mask_immediate_instruction(gcore):
    # r3 = 0xFF AND NOT 0x01 == 0xFE
    gcore.r[1] = 0xFF
    immed = 0x01
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, immed, "immediate")
    gcore.execute(instr)
    assert gcore.r[3] == 0xFE

    # r3 = 0xFF AND NOT 0x7F == 0x80
    gcore.r[1] = 0xFF
    immed = 0x7F
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, immed, "immediate")
    gcore.execute(instr)
    assert gcore.r[3] == 0x80

    # r3 = 0xAA AND NOT 0xF0 == 0x0A
    gcore.r[1] = 0xAA
    immed = 0xF0
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, immed, "immediate")
    gcore.execute(instr)
    assert gcore.r[3] == 0x0A

    # r3 = 0xAA AND NOT 0x0F == 0xA0
    gcore.r[1] = 0xAA
    immed = 0x0F
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, immed, "immediate")
    gcore.execute(instr)
    assert gcore.r[3] == 0xA0


def test_mask_register_instruction(gcore):
    # r3 = r1(0xFF) AND NOT r2(0x01) == 0xFE
    gcore.r[1] = 0xFF
    gcore.r[2] = 0x01
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0xFE

    # r3 = r1(0xFF) AND NOT r2(0x7F) == 0x80
    gcore.r[1] = 0xFF
    gcore.r[2] = 0x7F
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0x80

    # r3 = r1(0xAA) AND NOT r2(0xF0) == 0x0A
    gcore.r[1] = 0xAA
    gcore.r[2] = 0xF0
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0x0A

    # r3 = r1(0xAA) AND NOT r2(0x0F) == 0xA0
    gcore.r[1] = 0xAA
    gcore.r[2] = 0x0F
    gcore.r[3] = 0
    instr = INSTR("mask", None, 3, 1, 2, "register")
    gcore.execute(instr)
    assert gcore.r[3] == 0xA0


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


def test_ret_instructino(gcore):
    pass


def test_reti_instructino(gcore):
    pass


def test_enai_instructino(gcore):
    assert gcore.IREN == False

    instr = INSTR("enai", None, None, None, None, None)
    gcore.execute(instr)
    assert gcore.IREN == True

    gcore.execute(instr)
    assert gcore.IREN == True


def test_disi_instructino(gcore):
    gcore.IREN = True
    assert gcore.IREN == True

    instr = INSTR("disi", None, None, None, None, None)
    gcore.execute(instr)
    assert gcore.IREN == False

    gcore.execute(instr)
    assert gcore.IREN == False


def test_wait_instructino(gcore):
    assert gcore.WAIT == False

    instr = INSTR("wait", None, None, None, None, None)
    gcore.execute(instr)
    assert gcore.WAIT == True

    gcore.execute(instr)
    assert gcore.WAIT == True


def test_stby_instructino(gcore):
    assert gcore.STBY == False

    instr = INSTR("stby", None, None, None, None, None)
    gcore.execute(instr)
    assert gcore.STBY == True

    gcore.execute(instr)
    assert gcore.STBY == True


def test_ldm_instruction(gcore):
    # direct access
    # rd = 2, op1 = r1, op2 = 0
    instr = INSTR("ldm", None, 2, 1, 0, None)
    gcore.r[1] = 0

    assert gcore.r[2] == 0
    gcore.execute(instr)
    assert gcore.r[2] == 0

    gcore.data_memory[0] = 1
    gcore.execute(instr)
    assert gcore.r[2] == 1

    gcore.data_memory[0xAB] = 0xCD
    gcore.r[1] = 0xAB
    gcore.execute(instr)
    assert gcore.r[2] == 0xCD

    # offset access
    # rd = 2, op1 = r1, op2 = 1
    gcore.r[1] = 0xAB
    instr = INSTR("ldm", None, 2, 1, 1, None)
    gcore.data_memory[0xAB] = 0xCD
    gcore.data_memory[0xAC] = 0xEF
    gcore.data_memory[0xAD] = 0x12
    gcore.execute(instr)
    assert gcore.r[2] == 0xEF

    instr = INSTR("ldm", None, 2, 1, 2, None)
    gcore.execute(instr)
    assert gcore.r[2] == 0x12


def test_stm_instruction(gcore):
    # direct access
    # rd = r2, op1 = r1, op2 = 0
    instr = INSTR("stm", None, 2, 1, 0, None)
    gcore.r[1] = 0
    gcore.r[2] = 0xAB

    gcore.execute(instr)
    assert gcore.data_memory[0] == 0xAB

    gcore.r[1] = 10
    gcore.r[2] = 0xCD

    gcore.execute(instr)
    assert gcore.data_memory[10] == 0xCD

    # offset access
    # rd = r2, op1 = r1, op2 = 1
    gcore.r[1] = 0
    gcore.r[2] = 0xEF
    instr = INSTR("stm", None, 2, 1, 1, None)

    gcore.execute(instr)
    assert gcore.data_memory[1] == 0xEF


def test_inp_instruction(gcore):
    # rd = r2, op1 = r1, op2 = 0
    instr = INSTR("inp", None, 2, 1, 0, None)
    gcore.r[1] = 0
    gcore.r[2] = 0
    gcore.IO_controller_register[0] = 0xAB
    gcore.execute(instr)
    assert gcore.r[2] == 0xAB


def test_out_instruction(gcore):
    # rd = r2, op1 = r1, op2 = 0
    instr = INSTR("out", None, 2, 1, 0, None)
    gcore.r[1] = 0
    gcore.r[2] = 0xAB
    gcore.execute(instr)
    assert gcore.IO_controller_register[0] == 0xAB
