__author__ = 'BW'

# Add current directory to PYTHONPATH
import os, sys
sys.path.insert(0, os.getcwd())
#print('sys.path = ', sys.path)

import unittest

from GumnutSimulator import GumnutDecoder


class TestGumnutDecoder(unittest.TestCase):
    def test_decode_instructions(self):
        dec = GumnutDecoder.GumnutDecoder()

        # Arithmetic/Logic
        # register access
        self.assertEqual(dec.decode_instruction(0x38A60), GumnutDecoder.INSTR('add', 0, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A61), GumnutDecoder.INSTR('addc', 1, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A62), GumnutDecoder.INSTR('sub', 2, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A63), GumnutDecoder.INSTR('subc', 3, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A64), GumnutDecoder.INSTR('and', 4, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A65), GumnutDecoder.INSTR('or', 5, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A66), GumnutDecoder.INSTR('xor', 6, 1, 2, 3, 'register'))
        self.assertEqual(dec.decode_instruction(0x38A67), GumnutDecoder.INSTR('mask', 7, 1, 2, 3, 'register'))
        # add r8, r9, r10 will cause an jmp to 0x2368
        # self.assertEqual(dec.decode_instruction(248128), GumnutDecoder.INSTR('add', 0, 8, 9, 10, 'register'))

        # immediate access
        self.assertEqual(dec.decode_instruction(0x0),    GumnutDecoder.INSTR('add', 0, 0, 0, 0, 'immediate'))
        self.assertEqual(dec.decode_instruction(0xA12),  GumnutDecoder.INSTR('add', 0, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0x4A12), GumnutDecoder.INSTR('addc', 1, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0x8A12), GumnutDecoder.INSTR('sub', 2, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0xCA12), GumnutDecoder.INSTR('subc', 3, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0x10A12), GumnutDecoder.INSTR('and', 4, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0x14A12), GumnutDecoder.INSTR('or', 5, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0x18A12), GumnutDecoder.INSTR('xor', 6, 1, 2, 18, 'immediate'))
        self.assertEqual(dec.decode_instruction(0x1CA12), GumnutDecoder.INSTR('mask', 7, 1, 2, 18, 'immediate'))

        # Shift instructions
        self.assertEqual(dec.decode_instruction(0x30000),  GumnutDecoder.INSTR('shl', 0, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x30a80),  GumnutDecoder.INSTR('shl', 0, 1, 2, 4, None))
        self.assertEqual(dec.decode_instruction(0x30a81),  GumnutDecoder.INSTR('shr', 1, 1, 2, 4, None))
        self.assertEqual(dec.decode_instruction(0x30a82),  GumnutDecoder.INSTR('rol', 2, 1, 2, 4, None))
        self.assertEqual(dec.decode_instruction(0x30a83),  GumnutDecoder.INSTR('ror', 3, 1, 2, 4, None))

        # Memory and I/O instructions
        # Direct offset
        self.assertEqual(dec.decode_instruction(0x20812),  GumnutDecoder.INSTR('ldm', 0, 1, 0, 18, None))
        self.assertEqual(dec.decode_instruction(0x24812),  GumnutDecoder.INSTR('stm', 1, 1, 0, 18, None))
        self.assertEqual(dec.decode_instruction(0x28812),  GumnutDecoder.INSTR('inp', 2, 1, 0, 18, None))
        self.assertEqual(dec.decode_instruction(0x2C812),  GumnutDecoder.INSTR('out', 3, 1, 0, 18, None))
        # Register + offset
        self.assertEqual(dec.decode_instruction(0x20a12),  GumnutDecoder.INSTR('ldm', 0, 1, 2, 18, None))
        self.assertEqual(dec.decode_instruction(0x24a12),  GumnutDecoder.INSTR('stm', 1, 1, 2, 18, None))
        self.assertEqual(dec.decode_instruction(0x28a12),  GumnutDecoder.INSTR('inp', 2, 1, 2, 18, None))
        self.assertEqual(dec.decode_instruction(0x2ca12),  GumnutDecoder.INSTR('out', 3, 1, 2, 18, None))

        # Branch instructions
        self.assertEqual(dec.decode_instruction(0x3e0ff),  GumnutDecoder.INSTR('bz', 0, 0, 0, 255, None))
        self.assertEqual(dec.decode_instruction(0x3e000),  GumnutDecoder.INSTR('bz', 0, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3e080),  GumnutDecoder.INSTR('bz', 0, 0, 0, 128, None))
        self.assertEqual(dec.decode_instruction(0x3e4ff),  GumnutDecoder.INSTR('bnz', 1, 0, 0, 255, None))
        self.assertEqual(dec.decode_instruction(0x3e400),  GumnutDecoder.INSTR('bnz', 1, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3e47f),  GumnutDecoder.INSTR('bnz', 1, 0, 0, 127, None))
        self.assertEqual(dec.decode_instruction(0x3e8ff),  GumnutDecoder.INSTR('bc', 2, 0, 0, 255, None))
        self.assertEqual(dec.decode_instruction(0x3e800),  GumnutDecoder.INSTR('bc', 2, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3e87f),  GumnutDecoder.INSTR('bc', 2, 0, 0, 127, None))
        self.assertEqual(dec.decode_instruction(0x3eCff),  GumnutDecoder.INSTR('bnc', 3, 0, 0, 255, None))
        self.assertEqual(dec.decode_instruction(0x3eC00),  GumnutDecoder.INSTR('bnc', 3, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3eC7f),  GumnutDecoder.INSTR('bnc', 3, 0, 0, 127, None))

        # Jump instructions
        self.assertEqual(dec.decode_instruction(0x3c000),  GumnutDecoder.INSTR('jmp', 0, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3cFFF),  GumnutDecoder.INSTR('jmp', 0, 0, 0, 4095, None))
        self.assertEqual(dec.decode_instruction(0x3d000),  GumnutDecoder.INSTR('jsb', 1, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3dFFF),  GumnutDecoder.INSTR('jsb', 1, 0, 0, 4095, None))

        # Misc instructions
        self.assertEqual(dec.decode_instruction(0x3F000),  GumnutDecoder.INSTR('ret', 0, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3F100),  GumnutDecoder.INSTR('reti', 1, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3F200),  GumnutDecoder.INSTR('enai', 2, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3F300),  GumnutDecoder.INSTR('disi', 3, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3F400),  GumnutDecoder.INSTR('wait', 4, 0, 0, 0, None))
        self.assertEqual(dec.decode_instruction(0x3F500),  GumnutDecoder.INSTR('stby', 5, 0, 0, 0, None))

if __name__ == "__main__":
    unittest.main() # run all tests
