import os

def test_help():
	exit_status = os.system(r'python GumnutSimulator\GumnutAssembler.py --help')
	assert exit_status == 0

def test_cli():
	exit_status = os.system(r'python GumnutSimulator\GumnutAssembler.py test\asm_source\sample.gsm')
	assert exit_status == 0

def test_cli_multiple():
	exit_status = os.system(r'python GumnutSimulator\GumnutAssembler.py test\asm_source\sample.gsm test\asm_source\jmp.gsm')
	assert exit_status == 0	

def test_cli_out_dir():
	exit_status = os.system(r'python GumnutSimulator\GumnutAssembler.py test\asm_source\sample.gsm -o test\asm_output_cli')
	assert exit_status == 0