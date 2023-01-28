import random
import cocotb
# import cocotb_coverage.coverage
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
from ialu_cmd import Scr1IaluCmdSelE

ALU_WIDTH = 32
TEST_ITER_COUNT = 5

def add_model(op1, op2):
    """model of an adder"""
    return (op1 + op2) & ((1 << ALU_WIDTH) - 1)

def sub_model(op1, op2):
    """model of a subtractor"""
    return (op1 - op2) & ((1 << ALU_WIDTH) - 1)

def apply_rand_in(op1, op2):
    """Set op1 and op2 to random 32 bit values"""
    op1.value = random.getrandbits(ALU_WIDTH)
    op2.value = random.getrandbits(ALU_WIDTH)

@cocotb.test()
async def adder_rand(dut):
    """Perform iALU add test"""

    log = cocotb.logging.getLogger("cocotb.test")

    sim_step = Timer(1)

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    res = dut.ialu2exu_main_res_o
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value
    cmd_model = add_model

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.info('%0x + %0x = %0x', op1.value, op2.value, res.value)
        assert res.value == cmd_model(op1.value, op2.value)

    raise TestSuccess

@cocotb.test()
async def sub_rand(dut):
    """Perform iALU subtract test"""

    log = cocotb.logging.getLogger("cocotb.test")

    sim_step = Timer(1)

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    res = dut.ialu2exu_main_res_o
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB.value
    cmd_model = sub_model

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.info('%0x - %0x = %0x', op1.value, op2.value, res.value)
        assert res.value == cmd_model(op1.value, op2.value)

    raise TestSuccess
