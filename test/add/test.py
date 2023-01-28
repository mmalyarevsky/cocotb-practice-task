import random
import cocotb
# import cocotb_coverage.coverage
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
from ialu_cmd import Scr1IaluCmdSelE

ADDER_WIDTH = 32

def add_model(op1, op2):
    """model of an adder"""
    return (op1 + op2) & ((1 << ADDER_WIDTH) - 1)

@cocotb.test()
async def adder_rand(dut):
    """Perform iALU add test"""

    log = cocotb.logging.getLogger("cocotb.test")

    sim_step = Timer(1)

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    res = dut.ialu2exu_main_res_o

    for _ in range(10000):
        op1.value = random.getrandbits(ADDER_WIDTH)
        op2.value = random.getrandbits(ADDER_WIDTH)
        cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value
        await sim_step
        log.info('%0x + %0x = %0x', op1.value, op2.value, res.value)
        assert res.value == add_model(op1.value, op2.value)

    raise TestSuccess
