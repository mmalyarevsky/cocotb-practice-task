from random import getrandbits
import cocotb
# import cocotb_coverage.coverage
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
from include.ialu_cmd import Scr1IaluCmdSelE
from include.ialu_models import add_uint32_model, sub_lt_int32_model, \
                                sub_ltu_uint32_mode, sub_uint32_model

ALU_WIDTH = 32
TEST_ITER_COUNT = 10000

sim_step = Timer(1)

log = cocotb.logging.getLogger("cocotb.test")

def apply_rand_in(op1, op2):
    """Set op1 and op2 to random 32 bit values"""
    op1.value = getrandbits(ALU_WIDTH)
    op2.value = getrandbits(ALU_WIDTH)

@cocotb.test()
async def add_rand(dut):
    """Perform iALU add test"""

    log.setLevel('INFO')
    # log.setLevel('DEBUG')

    op1 = dut.op1
    op2 = dut.op2
    cmd = dut.cmd
    main_res = dut.main_res
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x + %0x = %0x', op1.value, op2.value, main_res.value)
        assert main_res.value == add_uint32_model(op1.value, op2.value)

    raise TestSuccess

@cocotb.test()
async def sub_rand(dut):
    """Perform iALU subtract test"""

    log.setLevel('INFO')
    # log.setLevel('DEBUG')

    op1 = dut.op1
    op2 = dut.op2
    cmd = dut.cmd
    main_res = dut.main_res
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x - %0x = %0x', op1.value, op2.value, main_res.value)
        assert main_res.value == sub_uint32_model(op1.value, op2.value)

    raise TestSuccess

@cocotb.test()
async def sub_lt_rand(dut):
    """Perform iALU signed compare test"""

    log.setLevel('INFO')
    # log.setLevel('DEBUG')

    op1 = dut.op1
    op2 = dut.op2
    cmd = dut.cmd
    cmp_res = dut.cmp_res
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB_LT.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x < %0x = %0x', op1.value, op2.value, cmp_res.value)
        assert cmp_res.value == sub_lt_int32_model(op1.value, op2.value)

    raise TestSuccess

@cocotb.test()
async def sub_ltu_rand(dut):
    """Perform iALU unsigned compare test"""

    log.setLevel('INFO')
    # log.setLevel('DEBUG')

    op1 = dut.op1
    op2 = dut.op2
    cmd = dut.cmd
    cmp_res = dut.cmp_res
    cmd.value = Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB_LTU.value

    for _ in range(TEST_ITER_COUNT):
        apply_rand_in(op1, op2)
        await sim_step
        log.debug('%0x u< %0x = %0x', op1.value, op2.value, cmp_res.value)
        assert cmp_res.value == sub_ltu_uint32_mode(op1.value, op2.value)

    raise TestSuccess
