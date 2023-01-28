import random
import cocotb
import numpy as np
# import cocotb_coverage.coverage
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
from ialu_cmd import Scr1IaluCmdSelE

ALU_WIDTH = 32
TEST_ITER_COUNT = 10000

sim_step = Timer(1)

log = cocotb.logging.getLogger("cocotb.test")

def apply_rand_in(op1, op2):
    """Set op1 and op2 to random 32 bit values"""
    op1.value = random.getrandbits(ALU_WIDTH)
    op2.value = random.getrandbits(ALU_WIDTH)

def add_model(op1, op2):
    """model of an adder"""
    return (op1 + op2) & ((1 << ALU_WIDTH) - 1)

@cocotb.test()
async def add_rand(dut):
    """Perform iALU add test"""

    # log.setLevel('DEBUG')

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    res = dut.ialu2exu_main_res_o
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x + %0x = %0x', op1.value, op2.value, res.value)
        assert res.value == add_model(op1.value, op2.value)

    raise TestSuccess

def sub_model(op1, op2):
    """model of a subtractor"""
    return (op1 - op2) & ((1 << ALU_WIDTH) - 1)

@cocotb.test()
async def sub_rand(dut):
    """Perform iALU subtract test"""

    # log.setLevel('DEBUG')

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    res = dut.ialu2exu_main_res_o
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x - %0x = %0x', op1.value, op2.value, res.value)
        assert res.value == sub_model(op1.value, op2.value)

    raise TestSuccess

def sub_lt_model(op1, op2):
    """returns result of signed comparison: op1 < op2"""
    cmp1 = np.array(op1.value).astype(np.int32)
    cmp2 = np.array(op2.value).astype(np.int32)
    if cmp1 < cmp2:
        return 1
    return 0

@cocotb.test()
async def sub_lt_rand(dut):
    """Perform iALU signed compare test"""

    # log.setLevel('DEBUG')

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    cmp_res = dut.ialu2exu_main_res_o
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB_LT.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x < %0x = %0x', op1.value, op2.value, cmp_res.value)
        assert cmp_res.value == sub_lt_model(op1.value, op2.value)

    raise TestSuccess

def sub_ltu_model(op1, op2):
    """returns result of unsigned comparison: op1 < op2"""
    cmp1 = np.array(op1.value).astype(np.uint32)
    cmp2 = np.array(op2.value).astype(np.uint32)
    if cmp1 < cmp2:
        return 1
    return 0

@cocotb.test()
async def sub_ltu_rand(dut):
    """Perform iALU unsigned compare test"""

    # log.setLevel('DEBUG')

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    cmp_res = dut.ialu2exu_main_res_o
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB_LTU.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x u< %0x = %0x', op1.value, op2.value, cmp_res.value)
        assert cmp_res.value == sub_ltu_model(op1.value, op2.value)

    raise TestSuccess
