__author__ = 'BW'

# Add current directory to PYTHONPATH
import os
import sys
sys.path.insert(0, os.getcwd())
#print('sys.path = ', sys.path)


import unittest
import random
from GumnutSimulator import GumnutCore
from GumnutSimulator import GumnutExceptions


class TestGumnutCore(unittest.TestCase):

    def test_fetch_limits(self):
        core = GumnutCore.GumnutCore()
        core.PC = -1
        self.assertRaises(
            GumnutExceptions.InvalidPCValue, lambda: core.fetch())
        core.PC = 4098
        self.assertRaises(
            GumnutExceptions.InvalidPCValue, lambda: core.fetch())
        try:
            core.PC = 128
            core.fetch()
            raised = False
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_update_PC_limits(self):
        core = GumnutCore.GumnutCore()
        core.PC = 4093
        core.update_PC()    # 4094
        core.update_PC()    # 4095
        self.assertRaises(
            GumnutExceptions.InvalidPCValue, lambda: core.update_PC())  # 4096
        core.PC = -100
        self.assertRaises(
            GumnutExceptions.InvalidPCValue, lambda: core.update_PC())
        try:
            core.PC = 128
            core.update_PC()    # 129
            raised = False
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_unknown_instructions(self):
        # core = GumnutCore.GumnutCore()
        # ..
        pass

    def test_upload_instruction_memory(self):
        core = GumnutCore.GumnutCore()
        test_data = [int(1000 * random.random()) for i in range(4097)]
        self.assertRaises(GumnutExceptions.InstructionMemorySizeExceeded,
                          lambda: core.upload_instruction_memory(test_data))
        try:
            test_data = [int(1000 * random.random()) for i in range(4096)]
            core.upload_instruction_memory(test_data)
            raised = False
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_upload_data_memory(self):
        core = GumnutCore.GumnutCore()
        test_data = [int(1000 * random.random()) for i in range(257)]
        self.assertRaises(
            GumnutExceptions.DataMemorySizeExceeded,
            lambda: core.upload_data_memory(test_data))
        try:
            test_data = [int(1000 * random.random()) for i in range(256)]
            core.upload_data_memory(test_data)
            raised = False
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_check_data_memory_access(self):
        core = GumnutCore.GumnutCore()
        self.assertRaises(GumnutExceptions.DataMemoryAccessViolation,
                          lambda: core.check_data_memory_access(
                            core.data_memory_size + 1))
        try:
            core.check_data_memory_access(core.data_memory_size)
            raised = False
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_add_instruction(self):
        return
        core = GumnutCore.GumnutCore()

        # r1 = 1
        instr = GumnutCore.INSTR("add", 0, 1, 1, 1, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 1)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + 1 = 2
        instr = GumnutCore.INSTR("add", 0, 1, 1, 1, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 2)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + 254 = 256 -> CARRY & r1 = 0
        instr = GumnutCore.INSTR("add", 0, 1, 1, 254, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 0)
        self.assertEqual(core.CARRY, True)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + 2 = 2 -> CARRY == False
        instr = GumnutCore.INSTR("add", 0, 1, 1, 2, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 2)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + r1 = 4 -> CARRY == False
        instr = GumnutCore.INSTR("add", 0, 1, 1, 1, "register")
        core.execute(instr)
        self.assertEqual(core.r[1], 4)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

    def test_addc_instruction(self):
        return
        core = GumnutCore.GumnutCore()

        # r1 = 1
        instr = GumnutCore.INSTR("addc", 0, 1, 1, 1, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 1)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + 1 = 2
        instr = GumnutCore.INSTR("addc", 0, 1, 1, 1, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 2)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + 254 = 256 -> CARRY & r1 = 0
        instr = GumnutCore.INSTR("addc", 0, 1, 1, 254, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 0)
        self.assertEqual(core.CARRY, True)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + 2 = 2 -> CARRY == False
        instr = GumnutCore.INSTR("addc", 0, 1, 1, 2, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 3)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 + r1 = 6 -> CARRY == False
        instr = GumnutCore.INSTR("addc", 0, 1, 1, 1, "register")
        core.execute(instr)
        self.assertEqual(core.r[1], 6)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

    def test_sub_instruction(self):
        return
        core = GumnutCore.GumnutCore()

        # r1 = 1
        instr = GumnutCore.INSTR("add", 0, 1, 1, 1, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 1)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 - 4 = -3 -> CARRY & r1 = 253
        instr = GumnutCore.INSTR("sub", 0, 1, 1, 4, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 253)
        self.assertEqual(core.CARRY, True)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 - 4 = 249 -> CARRY == False
        instr = GumnutCore.INSTR("sub", 0, 1, 1, 4, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 249)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 - r1 = 0 -> CARRY == False
        instr = GumnutCore.INSTR("sub", 0, 1, 1, 1, "register")
        core.execute(instr)
        self.assertEqual(core.r[1], 0)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, True)

    def test_subc_instruction(self):
        return
        core = GumnutCore.GumnutCore()

        # r1 = 1
        instr = GumnutCore.INSTR("add", 0, 1, 1, 1, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 1)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 - 4 = -3 -> CARRY & r1 = 253
        instr = GumnutCore.INSTR("subc", 0, 1, 1, 4, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 253)
        self.assertEqual(core.CARRY, True)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 - 4 = 249 -> CARRY == False
        instr = GumnutCore.INSTR("subc", 0, 1, 1, 4, "immediate")
        core.execute(instr)
        self.assertEqual(core.r[1], 248)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, False)

        # r1 = r1 - r1 = 0 -> CARRY == False
        instr = GumnutCore.INSTR("subc", 0, 1, 1, 1, "register")
        core.execute(instr)
        self.assertEqual(core.r[1], 0)
        self.assertEqual(core.CARRY, False)
        self.assertEqual(core.ZERO, True)


if __name__ == "__main__":
    unittest.main()  # run all tests
