__author__ = 'BW'

# Add current directory to PYTHONPATH
import os, sys
sys.path.insert(0, os.getcwd())
#print('sys.path = ', sys.path)
print('sys.path = ', sys.path)

import unittest

from GumnutSimulator import GumnutAssembler


class TestGumnutAssembler(unittest.TestCase):

    def test_check_number(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._check_number('0'),0)
        self.assertEqual(asm._check_number('1'),1)
        self.assertEqual(asm._check_number('15'),15)
        self.assertEqual(asm._check_number('255'),255)
        self.assertEqual(asm._check_number('0x0'),0)
        self.assertEqual(asm._check_number('0x1'),1)
        self.assertEqual(asm._check_number('0xF'),15)
        self.assertEqual(asm._check_number('0xFF'),255)
        self.assertEqual(asm._check_number('0b0'),0)
        self.assertEqual(asm._check_number('0b1'),1)
        self.assertEqual(asm._check_number('0b1111'),0xF)
        self.assertEqual(asm._check_number('0b11111111'),0xFF)
        self.assertEqual(asm._check_number('-1'), 0xFF)
        #self.assertEqual(asm._check_number('-3'), 0xFFFFFFFD)
        #self.assertEqual(asm._check_number('-255'), 1)
        self.assertEqual(asm._check_number('+1'),+1)
        self.assertEqual(asm._check_number('+255'),+255)

        self.assertEqual(asm._check_number('r0'), 'r0')
        self.assertEqual(asm._check_number('reference'), 'reference')
        self.assertEqual(asm._check_number('label:'), 'label:')

        self.assertEqual(asm._check_number('0.123'), -1)
        self.assertEqual(asm._check_number('0,123'), -1)
        self.assertEqual(asm._check_number('+0.123'), -1)
        self.assertEqual(asm._check_number('+0,123'), -1)
        self.assertEqual(asm._check_number('-0.123'), -1)
        self.assertEqual(asm._check_number('-0,123'), -1)


    def test_extract_identifier_from_line(self):
        asm = GumnutAssembler.GumnutAssembler()
        GasmLine = GumnutAssembler.GasmLine
        # ..
        self.assertEqual(asm._extract_identifier_from_line("; Comment org 0x1"), GasmLine(None, None, None, None, None))

        # ..
        self.assertEqual(asm._extract_identifier_from_line("org 0x1"), GasmLine(None, "org", 1, None, None))
        self.assertEqual(asm._extract_identifier_from_line("bigdec1024: byte 1024"), GasmLine("bigdec1024", "byte", 1024, None, None))
        self.assertEqual(asm._extract_identifier_from_line("null0: byte 0"), GasmLine("null0", "byte", 0, None, None))
        self.assertEqual(asm._extract_identifier_from_line("neg_1: byte -1"), GasmLine("neg_1", "byte", 0xFF, None, None))

        # Arithemtic and logical instructions
        # Register access
        self.assertEqual(asm._extract_identifier_from_line("add r0, r0, r0"), GasmLine(None, "add", "r0", "r0", "r0"))
        self.assertEqual(asm._extract_identifier_from_line("add r0, r1, r2"), GasmLine(None, "add", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("addc r0, r1, r2"), GasmLine(None, "addc", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("sub r0, r1, r2"), GasmLine(None, "sub", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("subc r0, r1, r2"), GasmLine(None, "subc", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("and r0, r1, r2"), GasmLine(None, "and", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("or r0, r1, r2"), GasmLine(None, "or", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("xor r0, r1, r2"), GasmLine(None, "xor", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("mask r0, r1, r2"), GasmLine(None, "mask", "r0", "r1", "r2"))

        self.assertEqual(asm._extract_identifier_from_line("add r8, r9, r10"), GasmLine(None, "add", "r8", "r9", "r10"))
        # Immediate access
        self.assertEqual(asm._extract_identifier_from_line("add r0, r0, 0x0"), GasmLine(None, "add", "r0", "r0", 0))
        self.assertEqual(asm._extract_identifier_from_line("add r0, r1, 0x12"), GasmLine(None, "add", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("addc r0, r1, 0x12"), GasmLine(None, "addc", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("sub r0, r1, 0x12"), GasmLine(None, "sub", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("subc r0, r1, 0x12"), GasmLine(None, "subc", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("and r0, r1, 0x12"), GasmLine(None, "and", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("or r0, r1, 0x12"), GasmLine(None, "or", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("xor r0, r1, 0x12"), GasmLine(None, "xor", "r0", "r1", 18))
        self.assertEqual(asm._extract_identifier_from_line("mask r0, r1, 0x12"), GasmLine(None, "mask", "r0", "r1", 18))

        # Shift instructions
        self.assertEqual(asm._extract_identifier_from_line("shl r1, r2, 0x2"),
                         GasmLine(None, "shl", "r1", "r2", 2))
        self.assertEqual(asm._extract_identifier_from_line("shr r1, r2, 0x2"),
                         GasmLine(None, "shr", "r1", "r2", 2))
        self.assertEqual(asm._extract_identifier_from_line("rol r1, r2, 0x2"),
                         GasmLine(None, "rol", "r1", "r2", 2))
        self.assertEqual(asm._extract_identifier_from_line("ror r1, r2, 0x2"),
                         GasmLine(None, "ror", "r1", "r2", 2))

        # Memory and I/O instructions
        # Direct access
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, 0x12"),GasmLine(None, "ldm", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("stm r1, 0x12"),GasmLine(None, "stm", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("inp r1, 0x12"),GasmLine(None, "inp", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("out r1, 0x12"),GasmLine(None, "out", "r1", 18, None))
        # Register + offset
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, (r2) + 0x12"),GasmLine(None, "ldm", "r1", "r2", 18))
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, (r2) - 0x12"),GasmLine(None, "ldm", "r1", "r2", 0xEE))
        self.assertEqual(asm._extract_identifier_from_line("stm r1, (r2) + 0x12"),GasmLine(None, "stm", "r1", "r2", 18))
        self.assertEqual(asm._extract_identifier_from_line("inp r1, (r2) + 0x12"),GasmLine(None, "inp", "r1", "r2", 18))
        self.assertEqual(asm._extract_identifier_from_line("out r1, (r2) + 0x12"),GasmLine(None, "out", "r1", "r2", 18))
        # Reference
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, start_val"),GasmLine(None, "ldm", "r1", "start_val", None))
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, (start_val)+0x12"),GasmLine(None, "ldm", "r1", "start_val", 18))
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, (start_val)-0x12"),GasmLine(None, "ldm", "r1", "start_val", 0xEE))

        # Branch instructions
        self.assertEqual(asm._extract_identifier_from_line("bz 12"), GasmLine(None, "bz", 12, None, None))
        #self.assertEqual(parser._extract_identifier_from_line("bz -12"),parser.ASMLINE(None,"bz","-12",None,None))
        self.assertEqual(asm._extract_identifier_from_line("bnz 12"), GasmLine(None, "bnz", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bnz -12"),parser.ASMLINE(None,"bnz","-12",None,None))
        self.assertEqual(asm._extract_identifier_from_line("bc 12"), GasmLine(None, "bc", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bc -12"),parser.ASMLINE(None,"bc","-12",None,None))
        self.assertEqual(asm._extract_identifier_from_line("bnc 12"), GasmLine(None, "bnc", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bnc -12"),parser.ASMLINE(None,"bnc","-12",None,None))

        # Jump instructions
        self.assertEqual(asm._extract_identifier_from_line("jmp 0xFC12"),
                         GasmLine(None, "jmp", 64530, None, None))
        self.assertEqual(asm._extract_identifier_from_line("jsb 0xFC12"),
                         GasmLine(None, "jsb", 64530, None, None))

        # Empty lines, comments and labels
        self.assertEqual(asm._extract_identifier_from_line(""), GasmLine(None, None, None, None, None))
        self.assertEqual(asm._extract_identifier_from_line(";Comment"), GasmLine(None, None, None, None, None))
        self.assertEqual(asm._extract_identifier_from_line("label:"), GasmLine("label", None, None, None, None))
        self.assertEqual(asm._extract_identifier_from_line("label: add r0, r1, r2"), GasmLine("label", "add", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("label: bz 0x12"), GasmLine("label", "bz", 18, None, None))
        self.assertEqual(asm._extract_identifier_from_line("label: ldm r1, 0x12"), GasmLine("label", "ldm", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("label: add r0, r1, r2"), GasmLine("label", "add", "r0", "r1", "r2"))
        self.assertEqual(asm._extract_identifier_from_line("label: out r1, (r2) + 0x12"),GasmLine("label", "out", "r1", "r2", 18))
        # ... um fehlerhafte Eingaben erweitern


    def test_get_register_number(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._get_register_number(None), -1)
        self.assertEqual(asm._get_register_number("r0"), 0)
        self.assertEqual(asm._get_register_number("r2"), 2)
        self.assertEqual(asm._get_register_number("r1024"), 1024)   # Muss False liefern
        self.assertEqual(asm._get_register_number("register0"), -1)
        self.assertEqual(asm._get_register_number("varname"), -1)
        self.assertEqual(asm._get_register_number("0x12"), -1)
        self.assertEqual(asm._get_register_number("12"), -1)
        self.assertEqual(asm._get_register_number(12), -1)


    def test_check_if_immedinstr(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._check_if_immed_instr("r2"), False)
        self.assertEqual(asm._check_if_immed_instr("register0"), False)
        self.assertEqual(asm._check_if_immed_instr("varname"), False)
        self.assertEqual(asm._check_if_immed_instr(18), True)
        self.assertEqual(asm._check_if_immed_instr(12), True)


    def test_check_operand_for_reference(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._check_operand_for_reference(None), False)
        self.assertEqual(asm._check_operand_for_reference("label"), True)
        self.assertEqual(asm._check_operand_for_reference("value_1"), True)
        self.assertEqual(asm._check_operand_for_reference("r0"), False)
        self.assertEqual(asm._check_operand_for_reference("r1"), False)
        self.assertEqual(asm._check_operand_for_reference("0x12"), False)
        self.assertEqual(asm._check_operand_for_reference("0b1101"), False)
        self.assertEqual(asm._check_operand_for_reference("22"), False)


    def test_get_reference(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._get_reference(None), False)
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._get_reference("label"), False)
        self.assertEqual(asm.NeedSecondRun, True)
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._get_reference("value_1"), False)
        self.assertEqual(asm.NeedSecondRun, True)
        self.assertEqual(asm._get_reference("r0"), False)
        self.assertEqual(asm._get_reference("r1"), False)
        self.assertEqual(asm._get_reference("0x12"), False)
        self.assertEqual(asm._get_reference("0b1101"), False)
        self.assertEqual(asm._get_reference("22"), False)
        # ..


    def test_assemble_source_line(self):
        asm = GumnutAssembler.GumnutAssembler()
        GasmLine = GumnutAssembler.GasmLine

        # Arithemtic and logical instructions
        # Register access
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"add","r1","r2","r3")),0x38A60)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"addc","r1","r2","r3")),0x38A61)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"sub","r1","r2","r3")),0x38A62)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"subc","r1","r2","r3")),0x38A63)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"and","r1","r2","r3")),0x38A64)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"or","r1","r2","r3")),0x38A65)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"xor","r1","r2","r3")),0x38A66)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"mask","r1","r2","r3")),0x38A67)

        self.assertEqual(asm._assemble_source_line(GasmLine(None,"add","r8","r9","r10")),248128)

        # Immediate access
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"add","r1","r2", 0x12)),0xA12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"addc","r1","r2", 0x12)),0x4A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"sub","r1","r2", 0x12)),0x8A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"subc","r1","r2", 0x12)),0xCA12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"and","r1","r2", 0x12)),0x10A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"or","r1","r2", 0x12)),0x14A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"xor","r1","r2", 0x12)),0x18A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"mask","r1","r2", 0x12)),0x1CA12)

        # Shift instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"shl","r1","r2",0x12)),0x30a40)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"shr","r1","r2",0x12)),0x30a41)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"rol","r1","r2",0x12)),0x30a42)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"ror","r1","r2",0x12)),0x30a43)

        # Memory and I/O instructions
        # Direct offset
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"ldm","r1",0x12, None)),0x20812)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"stm","r1",0x12, None)),0x24812)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"inp","r1",0x12, None)),0x28812)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"out","r1",0x12, None)),0x2c812)
        # Register + offset
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"ldm","r1","r2", 0x12)),0x20a12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"stm","r1","r2", 0x12)),0x24a12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"inp","r1","r2", 0x12)),0x28a12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"out","r1","r2", 0x12)),0x2Ca12)

        # Branch instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bz",0x00,None, None)),0x3e0ff)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bz",0x01,None, None)),0x3e000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bz",0x80,None, None)),0x3e07f)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bz",0x00,None, None)),0x3e0ef)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bz",0x01,None, None)),0x3e0f0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bz",0x80,None, None)),0x3e06f)
        asm.InstrMemPointer = 0x00
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnz",0x00,None, None)),0x3e4ff)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnz",0x01,None, None)),0x3e400)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnz",0x80,None, None)),0x3e47f)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnz",0x00,None, None)),0x3e4ef)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnz",0x01,None, None)),0x3e4f0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnz",0x80,None, None)),0x3e46f)
        asm.InstrMemPointer = 0x00
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bc",0x00,None, None)),0x3e8ff)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bc",0x01,None, None)),0x3e800)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bc",0x80,None, None)),0x3e87f)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bc",0x00,None, None)),0x3e8ef)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bc",0x01,None, None)),0x3e8f0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bc",0x80,None, None)),0x3e86f)
        asm.InstrMemPointer = 0x00
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnc",0x00,None, None)),0x3eCff)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnc",0x01,None, None)),0x3eC00)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnc",0x80,None, None)),0x3eC7f)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnc",0x00,None, None)),0x3eCef)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnc",0x01,None, None)),0x3eCf0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"bnc",0x80,None, None)),0x3eC6f)

        # Jump instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"jmp",0x00,None, None)),0x3c000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"jmp",0xFFF,None, None)),0x3cFFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"jmp",0xFFFF,None, None)),0x3cFFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"jsb",0x00,None, None)),0x3d000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"jsb",0xFFF,None, None)),0x3dFFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"jsb",0xFFFF,None, None)),0x3dFFF)

        # Misc instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"ret", None, None, None)),0x3F000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"reti", None, None, None)),0x3F100)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"enai", None, None, None)),0x3F200)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"disi", None, None, None)),0x3F300)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"wait", None, None, None)),0x3F400)
        self.assertEqual(asm._assemble_source_line(GasmLine(None,"stby", None, None, None)),0x3F500)



    def generate_md5(self, filename):
        import hashlib  # Import hashlib library (md5 method)
        import os       # Import os library (getcwd method)

        # Open,close, read file and calculate MD5 on its contents
        path=os.getcwd()+filename
        with open(path, 'rb') as f:
            data = f.read()
            return hashlib.md5(data).hexdigest()

        return -1


    def test_objectcode_comparison(self):
        import subprocess
        source_directory = 'tests/asm_source/'
        sample_sources = ['sample.gsm', 'sensor_isr.gsm', 'polling_loop.gsm',
                          'rtc_handler.gsm', 'jmp.gsm', 'bz_bnz.gsm', 'bc_bnc.gsm', 'ldm.gsm' ] #, 'limits.gsm'

        for source in sample_sources:
            asm = GumnutAssembler.GumnutAssembler()
            asm.load_asm_source_from_file(source_directory + source)
            asm.assemble()
            asm.create_output_files()

            # Move the generated files into the test/gasm/ directory
            subprocess.call(['mv', 'gasm_text.dat', 'tests/gasm/'])
            subprocess.call(['mv', 'gasm_data.dat', 'tests/gasm/'])

            # Call gasm assembler
            subprocess.call(['java', '-cp', 'tests/gasm/Gasm.jar:tests/gasm/antlr.jar:test/gasm/', 'Gasm', source_directory + source, '-t','tests/gasm/gasm_text_golden.dat','-d','tests/gasm/gasm_data_golden.dat'])

            # Create md5 hash and compare outputs
            self.assertEqual(self.generate_md5('/tests/gasm/gasm_text_golden.dat'), self.generate_md5('/tests/gasm/gasm_text.dat'))
            self.assertEqual(self.generate_md5('/tests/gasm/gasm_data_golden.dat'), self.generate_md5('/tests/gasm/gasm_data.dat'))


if __name__ == "__main__":
    unittest.main() # run all tests
