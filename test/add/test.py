import random
import cocotb
import cocotb_coverage.coverage
from cocotb.triggers import Timer
# from cocotb.clock import Clock
from cocotb.result import TestFailure, TestSuccess

def adder_model(op1: int, op2: int) -> int:
    """model of an adder"""
    return op1 + op2 & 0xFFFF_FFFF

@cocotb.test()
async def adder_rand(dut):
    """Perform iALU add test"""

    log = cocotb.logging.getLogger("cocotb.test")

    sim_step = Timer(1)

    op1 = dut.exu2ialu_main_op1_i
    op2 = dut.exu2ialu_main_op2_i
    cmd = dut.exu2ialu_cmd_i
    res = dut.ialu2exu_main_res_o

    for _ in range(100):
        op1.value = random.getrandbits(32)
        op2.value = random.getrandbits(32)
        cmd.value = 4
        await sim_step
        log.info('%x + %x = %x', op1.value, op2.value, res.value)
        assert res.value == adder_model(op1.value, op2.value)

    raise TestSuccess()
