import json
from collections import OrderedDict
from enum import IntEnum

from gumnut_assembler.assembler import GumnutAssembler
from gumnut_assembler.exceptions import UnknownInstruction

from gumnut_simulator import __version__
from gumnut_simulator.core import GumnutCore
from gumnut_simulator.exceptions import (
    EmptyReturnStack,
    InstructionMemorySizeExceeded,
    InvalidInstruction,
    ReturnAddressStackOverflow,
)


class SimulatorState(IntEnum):
    halt = 0
    idle = 1
    breakpoint = 2


class GumnutSimulator:
    """
    Class which holds simulator data and CPU
    """

    def __init__(self):
        self.CPU = GumnutCore()
        self.lsom_map = dict()
        self.lines_of_code = 0
        self.current_line = 0
        self.number_of_instructions = 0
        self.breakpoints = list()
        self.exception = None
        self.state = SimulatorState.halt
        self.asm_source = ""
        self.debug_symbols = OrderedDict()
        self.previous_PC = -1
        self.steps = 0

    def reset(self):
        """Reset the simulator and the CPU"""
        self.CPU.reset()
        self.lsom_map.clear()
        self.lines_of_code = 0
        self.number_of_instructions = 0
        self.current_line = 0
        self.breakpoints.clear()
        self.exception = None
        self.state = SimulatorState.halt
        self.asm_source = ""
        self.debug_symbols = OrderedDict()
        self.previous_PC = -1
        self.steps = 0

    def setup(self, source):
        """Initialize the CPU"""
        self.reset()
        try:
            assembler = GumnutAssembler()  # Create as a persistent member or only when needed here?
            assembler.load_asm_source(source)
            assembler.assemble()

            self.asm_source = source
            self.lsom_map = assembler.source_objectcode_map
            self.lines_of_code = assembler.ASMLineCount
            self.number_of_instructions = assembler.InstrCount / 2

            self.CPU.upload_data_memory(assembler.get_data_memory())
            self.CPU.upload_instruction_memory(assembler.get_instruction_memory())

            if self.number_of_instructions > 0:
                self.state = SimulatorState.idle
            else:
                self.state = SimulatorState.halt

            self.debug_symbols = assembler.source_objectcode_map

        except (InvalidInstruction, InstructionMemorySizeExceeded, UnknownInstruction) as e:
            self.exception = e
            self.state = SimulatorState.halt
            return False
        else:
            return True

    def step(self):
        """Triggers a single step of the CPU"""
        try:
            self.previous_PC = self.CPU.PC
            self.CPU.step()
            self.steps += 1
            if self.get_current_line() in self.breakpoints:
                self.state = SimulatorState.breakpoint
            else:
                self.state = SimulatorState.idle
        except (InvalidInstruction, EmptyReturnStack) as e:
            self.exception = e
            self.state = SimulatorState.halt
            return False
        except ReturnAddressStackOverflow as e:
            self.exception = e
            self.state = SimulatorState.breakpoint
            return True
        else:
            return True

    def get_flags(self):
        """
        Return CPU flags as a dict

        :return: ``{'CARRY': False, 'ZERO': True, 'WAIT': False, 'STBY': False, 'IEN': False}``
        """

        result = dict()
        result.update({"CARRY": self.CPU.CARRY})
        result.update({"ZERO": self.CPU.ZERO})
        result.update({"WAIT": self.CPU.WAIT})
        result.update({"STBY": self.CPU.STBY})
        result.update({"IREN": self.CPU.IREN})
        return result

    def get_register(self):
        """
        Return CPU register as a dict

        :return: ``{'r0': 0x01, 'r1': 0x20, ... , 'r7': 0xFF,
                    'PC': 0x34, 'SP': 0xA0, 'RAS': [0xF8, 0xF4, 0xB5', 0xF7, 0xC1 ]}``"""
        result = dict()

        for i in range(0, 8):
            register_name = "r" + str(i)
            result.update({register_name: self.CPU.r[i]})

        result.update({"PC": self.CPU.PC})
        result.update({"SP": self.CPU.SP})

        ras = list()
        for i in range(0, 8):
            ras.append(self.CPU.return_address_stack[i])
        result.update({"RAS": ras})

        return result

    def get_instruction_memory(self):
        """
        Return CPU instruction memory as a list

        :return: ``[F8, F4, B5, F7, C1, 97, ... , D8, D4, 86, 94, 9B]``"""
        return self.CPU.instruction_memory

    def get_data_memory(self):
        """
        Return CPU data memory as a list

        :return: ``[F8, F4, B5, F7, C1, 97, ... , D8, D4, 86, 94, 9B]``"""
        return self.CPU.data_memory

    def get_IO_controller_register(self):
        """
        Return IO controller register as a list
        """
        return self.CPU.IO_controller_register

    def set_IO_controller_register(self, address, value):
        self.CPU.IO_controller_register[address] = value

    def get_current_line(self):
        """
        Return the current line number by looking up the current instruction memory pointer
        """
        for line_number, value in self.lsom_map.items():
            if value[3] == self.CPU.PC:
                return line_number
        return -1

    def get_simulator_data(self):
        """Return some debug/additional information"""
        result = dict()
        result.update({"state": self.state})
        result.update({"lines_of_code": self.lines_of_code})
        result.update({"number_of_instructions": self.number_of_instructions})
        result.update({"current_line": self.get_current_line()})
        result.update({"breakpoints": self.get_breakpoints()})
        result.update({"data_memory_access_addr": self.CPU.data_memory_access_addr})
        result.update({"steps": self.steps})
        if self.CPU.instruction is not None and self.CPU.instruction.instruction == "jsb":
            current_ret_line = self._get_source_line_from_address(self.previous_PC + 1)
            result.update({"current_ret_line": current_ret_line})

        if self.exception:
            result.update({"exception": self.exception.as_dict()})
            self.exception = None
        return result

    def toggle_breakpoint(self, line_number):
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
        else:
            self.breakpoints.append(line_number)

    def get_breakpoints(self):
        """
        Return current breakpoints
        """
        return self.breakpoints

    def get_state(self):
        """
        Return current simulator state
        """
        return self.state

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def _get_source_line_from_address(self, address):
        for line_number, field in self.debug_symbols.items():
            if field[3] == address:
                return line_number
        return -1

    def trigger_interrupt(self):
        """
        Triggers an CPU interrupt by setting the internal flag
        """
        self.CPU.IR = True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Gumnut Simulator")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
        help="show the version number and exit",
    )

    parser.parse_args()

    return 0


if __name__ == "__main__":
    main()
