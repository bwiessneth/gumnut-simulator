__author__ = "BW"

# Add current directory to PYTHONPATH
import os, sys

sys.path.insert(0, os.getcwd())

import unittest
import shutil

from GumnutSimulator import GumnutAssembler


class TestGumnutAssembler(unittest.TestCase):
    def test_check_number(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._check_number("0"), 0)
        self.assertEqual(asm._check_number("1"), 1)
        self.assertEqual(asm._check_number("15"), 15)
        self.assertEqual(asm._check_number("255"), 255)
        self.assertEqual(asm._check_number("0x0"), 0)
        self.assertEqual(asm._check_number("0x1"), 1)
        self.assertEqual(asm._check_number("0xF"), 15)
        self.assertEqual(asm._check_number("0xFF"), 255)
        self.assertEqual(asm._check_number("0b0"), 0)
        self.assertEqual(asm._check_number("0b1"), 1)
        self.assertEqual(asm._check_number("0b1111"), 0xF)
        self.assertEqual(asm._check_number("0b11111111"), 0xFF)
        self.assertEqual(asm._check_number("-1"), 0xFF)
        # self.assertEqual(asm._check_number('-3'), 0xFFFFFFFD)
        # self.assertEqual(asm._check_number('-255'), 1)
        self.assertEqual(asm._check_number("+1"), +1)
        self.assertEqual(asm._check_number("+255"), +255)

        self.assertEqual(asm._check_number("r0"), "r0")
        self.assertEqual(asm._check_number("reference"), "reference")
        self.assertEqual(asm._check_number("label:"), "label:")

        self.assertEqual(asm._check_number("0.123"), -1)
        self.assertEqual(asm._check_number("0,123"), -1)
        self.assertEqual(asm._check_number("+0.123"), -1)
        self.assertEqual(asm._check_number("+0,123"), -1)
        self.assertEqual(asm._check_number("-0.123"), -1)
        self.assertEqual(asm._check_number("-0,123"), -1)

    def test_extract_identifier_from_line(self):
        asm = GumnutAssembler.GumnutAssembler()
        GasmLine = GumnutAssembler.GasmLine
        # ..
        self.assertEqual(asm._extract_identifier_from_line("; Comment org 0x1"), GasmLine(None, None, None, None, None))

        # ..
        self.assertEqual(asm._extract_identifier_from_line("org 0x1"), GasmLine(None, "org", 1, None, None))
        self.assertEqual(
            asm._extract_identifier_from_line("bigdec1024: byte 1024"), GasmLine("bigdec1024", "byte", 1024, None, None)
        )
        self.assertEqual(asm._extract_identifier_from_line("null0: byte 0"), GasmLine("null0", "byte", 0, None, None))
        self.assertEqual(
            asm._extract_identifier_from_line("neg_1: byte -1"), GasmLine("neg_1", "byte", 0xFF, None, None)
        )

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
        self.assertEqual(asm._extract_identifier_from_line("shl r1, r2, 0x2"), GasmLine(None, "shl", "r1", "r2", 2))
        self.assertEqual(asm._extract_identifier_from_line("shr r1, r2, 0x2"), GasmLine(None, "shr", "r1", "r2", 2))
        self.assertEqual(asm._extract_identifier_from_line("rol r1, r2, 0x2"), GasmLine(None, "rol", "r1", "r2", 2))
        self.assertEqual(asm._extract_identifier_from_line("ror r1, r2, 0x2"), GasmLine(None, "ror", "r1", "r2", 2))

        # Memory and I/O instructions
        # Direct access
        self.assertEqual(asm._extract_identifier_from_line("ldm r1, 0x12"), GasmLine(None, "ldm", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("stm r1, 0x12"), GasmLine(None, "stm", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("inp r1, 0x12"), GasmLine(None, "inp", "r1", 18, None))
        self.assertEqual(asm._extract_identifier_from_line("out r1, 0x12"), GasmLine(None, "out", "r1", 18, None))
        # Register + offset
        self.assertEqual(
            asm._extract_identifier_from_line("ldm r1, (r2) + 0x12"), GasmLine(None, "ldm", "r1", "r2", 18)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("ldm r1, (r2) - 0x12"), GasmLine(None, "ldm", "r1", "r2", 0xEE)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("stm r1, (r2) + 0x12"), GasmLine(None, "stm", "r1", "r2", 18)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("inp r1, (r2) + 0x12"), GasmLine(None, "inp", "r1", "r2", 18)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("out r1, (r2) + 0x12"), GasmLine(None, "out", "r1", "r2", 18)
        )
        # Reference
        self.assertEqual(
            asm._extract_identifier_from_line("ldm r1, start_val"), GasmLine(None, "ldm", "r1", "start_val", None)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("ldm r1, (start_val)+0x12"), GasmLine(None, "ldm", "r1", "start_val", 18)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("ldm r1, (start_val)-0x12"),
            GasmLine(None, "ldm", "r1", "start_val", 0xEE),
        )

        # Branch instructions
        self.assertEqual(asm._extract_identifier_from_line("bz 12"), GasmLine(None, "bz", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bz -12"),parser.ASMLINE(None,"bz","-12",None,None))
        self.assertEqual(asm._extract_identifier_from_line("bnz 12"), GasmLine(None, "bnz", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bnz -12"),parser.ASMLINE(None,"bnz","-12",None,None))
        self.assertEqual(asm._extract_identifier_from_line("bc 12"), GasmLine(None, "bc", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bc -12"),parser.ASMLINE(None,"bc","-12",None,None))
        self.assertEqual(asm._extract_identifier_from_line("bnc 12"), GasmLine(None, "bnc", 12, None, None))
        # self.assertEqual(parser._extract_identifier_from_line("bnc -12"),parser.ASMLINE(None,"bnc","-12",None,None))

        # Jump instructions
        self.assertEqual(asm._extract_identifier_from_line("jmp 0xFC12"), GasmLine(None, "jmp", 64530, None, None))
        self.assertEqual(asm._extract_identifier_from_line("jsb 0xFC12"), GasmLine(None, "jsb", 64530, None, None))

        # Empty lines, comments and labels
        self.assertEqual(asm._extract_identifier_from_line(""), GasmLine(None, None, None, None, None))
        self.assertEqual(asm._extract_identifier_from_line(";Comment"), GasmLine(None, None, None, None, None))
        self.assertEqual(asm._extract_identifier_from_line("label:"), GasmLine("label", None, None, None, None))
        self.assertEqual(
            asm._extract_identifier_from_line("label: add r0, r1, r2"), GasmLine("label", "add", "r0", "r1", "r2")
        )
        self.assertEqual(asm._extract_identifier_from_line("label: bz 0x12"), GasmLine("label", "bz", 18, None, None))
        self.assertEqual(
            asm._extract_identifier_from_line("label: ldm r1, 0x12"), GasmLine("label", "ldm", "r1", 18, None)
        )
        self.assertEqual(
            asm._extract_identifier_from_line("label: add r0, r1, r2"), GasmLine("label", "add", "r0", "r1", "r2")
        )
        self.assertEqual(
            asm._extract_identifier_from_line("label: out r1, (r2) + 0x12"), GasmLine("label", "out", "r1", "r2", 18)
        )
        # ... um fehlerhafte Eingaben erweitern

    def test_get_register_number(self):
        asm = GumnutAssembler.GumnutAssembler()
        self.assertEqual(asm._get_register_number(None), -1)
        self.assertEqual(asm._get_register_number("r0"), 0)
        self.assertEqual(asm._get_register_number("r2"), 2)
        self.assertEqual(asm._get_register_number("r1024"), 1024)  # Muss False liefern
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
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "add", "r1", "r2", "r3")), 0x38A60)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "addc", "r1", "r2", "r3")), 0x38A61)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "sub", "r1", "r2", "r3")), 0x38A62)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "subc", "r1", "r2", "r3")), 0x38A63)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "and", "r1", "r2", "r3")), 0x38A64)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "or", "r1", "r2", "r3")), 0x38A65)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "xor", "r1", "r2", "r3")), 0x38A66)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "mask", "r1", "r2", "r3")), 0x38A67)

        self.assertEqual(asm._assemble_source_line(GasmLine(None, "add", "r8", "r9", "r10")), 248128)

        # Immediate access
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "add", "r1", "r2", 0x12)), 0xA12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "addc", "r1", "r2", 0x12)), 0x4A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "sub", "r1", "r2", 0x12)), 0x8A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "subc", "r1", "r2", 0x12)), 0xCA12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "and", "r1", "r2", 0x12)), 0x10A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "or", "r1", "r2", 0x12)), 0x14A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "xor", "r1", "r2", 0x12)), 0x18A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "mask", "r1", "r2", 0x12)), 0x1CA12)

        # Shift instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "shl", "r1", "r2", 0x12)), 0x30A40)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "shr", "r1", "r2", 0x12)), 0x30A41)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "rol", "r1", "r2", 0x12)), 0x30A42)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "ror", "r1", "r2", 0x12)), 0x30A43)

        # Memory and I/O instructions
        # Direct offset
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "ldm", "r1", 0x12, None)), 0x20812)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "stm", "r1", 0x12, None)), 0x24812)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "inp", "r1", 0x12, None)), 0x28812)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "out", "r1", 0x12, None)), 0x2C812)
        # Register + offset
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "ldm", "r1", "r2", 0x12)), 0x20A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "stm", "r1", "r2", 0x12)), 0x24A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "inp", "r1", "r2", 0x12)), 0x28A12)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "out", "r1", "r2", 0x12)), 0x2CA12)

        # Branch instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bz", 0x00, None, None)), 0x3E0FF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bz", 0x01, None, None)), 0x3E000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bz", 0x80, None, None)), 0x3E07F)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bz", 0x00, None, None)), 0x3E0EF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bz", 0x01, None, None)), 0x3E0F0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bz", 0x80, None, None)), 0x3E06F)
        asm.InstrMemPointer = 0x00
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnz", 0x00, None, None)), 0x3E4FF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnz", 0x01, None, None)), 0x3E400)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnz", 0x80, None, None)), 0x3E47F)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnz", 0x00, None, None)), 0x3E4EF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnz", 0x01, None, None)), 0x3E4F0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnz", 0x80, None, None)), 0x3E46F)
        asm.InstrMemPointer = 0x00
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bc", 0x00, None, None)), 0x3E8FF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bc", 0x01, None, None)), 0x3E800)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bc", 0x80, None, None)), 0x3E87F)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bc", 0x00, None, None)), 0x3E8EF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bc", 0x01, None, None)), 0x3E8F0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bc", 0x80, None, None)), 0x3E86F)
        asm.InstrMemPointer = 0x00
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnc", 0x00, None, None)), 0x3ECFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnc", 0x01, None, None)), 0x3EC00)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnc", 0x80, None, None)), 0x3EC7F)
        asm.InstrMemPointer = 0x10
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnc", 0x00, None, None)), 0x3ECEF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnc", 0x01, None, None)), 0x3ECF0)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "bnc", 0x80, None, None)), 0x3EC6F)

        # Jump instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "jmp", 0x00, None, None)), 0x3C000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "jmp", 0xFFF, None, None)), 0x3CFFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "jmp", 0xFFFF, None, None)), 0x3CFFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "jsb", 0x00, None, None)), 0x3D000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "jsb", 0xFFF, None, None)), 0x3DFFF)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "jsb", 0xFFFF, None, None)), 0x3DFFF)

        # Misc instructions
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "ret", None, None, None)), 0x3F000)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "reti", None, None, None)), 0x3F100)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "enai", None, None, None)), 0x3F200)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "disi", None, None, None)), 0x3F300)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "wait", None, None, None)), 0x3F400)
        self.assertEqual(asm._assemble_source_line(GasmLine(None, "stby", None, None, None)), 0x3F500)

    def generate_md5(self, filename):
        import hashlib  # Import hashlib library (md5 method)
        import os  # Import os library (getcwd method)

        # Open,close, read file and calculate MD5 on its contents
        path = os.path.join(os.getcwd(), filename)
        with open(path, "rb") as f:
            data = f.read()
            return hashlib.md5(data).hexdigest()

        return -1

    def test_objectcode_comparison(self):
        import subprocess

        source_directory = "test/asm_source/"
        output_directory = "test/asm_output/"
        gasm_directory = "test/gasm_output/"
        sample_sources = [
            "sample.gsm",
            "sensor_isr.gsm",
            "polling_loop.gsm",
            "rtc_handler.gsm",
            "jmp.gsm",
            "bz_bnz.gsm",
            "bc_bnc.gsm",
            "ldm.gsm",
        ]  # , 'limits.gsm'

        for source in sample_sources:
            source_name, source_ext = os.path.splitext(source)
            datafile = os.path.join(output_directory, source_name + "_data.dat")
            textfile = os.path.join(output_directory, source_name + "_text.dat")
            gasm_datafile = os.path.join(gasm_directory, source_name + "_data.dat")
            gasm_textfile = os.path.join(gasm_directory, source_name + "_text.dat")

            asm = GumnutAssembler.GumnutAssembler()
            asm.load_asm_source_from_file(source_directory + source)
            asm.assemble()
            asm.create_output_files(datafile=datafile, textfile=textfile)

            # Call gasm assembler
            # subprocess.run(['java', '-classpath', 'test/gasm/Gasm.jar;test/gasm/antlr.jar;test/gasm/', 'Gasm', source_directory + source, '-t','test/gasm_output/'+source_name+'_text.dat','-d','test/gasm_output/'+source_name+'_data.dat'], shell=True, check=True)

            # Create md5 hash and compare outputs
            self.assertEqual(self.generate_md5(textfile), self.generate_md5(gasm_textfile))
            self.assertEqual(self.generate_md5(datafile), self.generate_md5(gasm_datafile))


if __name__ == "__main__":
    unittest.main()  # run all tests
