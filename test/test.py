# from random import getrandbits, randint, randrange
import cocotb
import numpy as np
# import cocotb_coverage.coverage
from cocotb.binary import BinaryValue
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
from include.ialu_cmd import Scr1IaluCmdSelE
from include.ialu_models import add_uint32_model, sub_uint32_model

ALU_WIDTH = 32
TEST_ITER_COUNT = 100000

sim_step = Timer(1)

def set_dut_controls(dut, cmd, op1, op2):
    "sets dut's signals to desired values"
    dut.cmd.value = cmd
    dut.op1.value = op1
    dut.op2.value = op2

@cocotb.test()
async def add_corners_simple(dut):
    """Perform iALU addition test with min and max op values"""

    corner_vlaues_list = [0x0, 0xFFFF_FFFF]

    for op1 in corner_vlaues_list:
        for op2 in corner_vlaues_list:

            set_dut_controls(dut, Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value, op1, op2)
            await sim_step

            assert dut.main_res.value == add_uint32_model(op1, op2)

    raise TestSuccess

@cocotb.test()
async def add_rand_overflow_corner(dut):
    """Perform iALU addition test where overflow occurs"""

    op1_bits_covered = BinaryValue(n_bits=32)
    op2_bits_covered = BinaryValue(n_bits=32)
    res_bits_covered = BinaryValue(n_bits=32)

    for _ in range(TEST_ITER_COUNT):
        ovflw_res = np.random.randint(1 << ALU_WIDTH, (1 << ALU_WIDTH + 1) - 2, dtype=np.uint64) # from 0x1_0000_0000 to 0x1_FFFF_FFFD
        op1 = np.random.randint(ovflw_res - (1 << ALU_WIDTH) + 1, (1 << ALU_WIDTH), dtype=np.uint32)
        op2 = ovflw_res - op1
        # print('op1 = ', hex(op1))
        # print('op2 = ', hex(op2))
        # print('ovflw_res = ', hex(ovflw_res))

        op1_binary = BinaryValue(n_bits=32)
        op2_binary = BinaryValue(n_bits=32)
        op1_binary.value = op1
        op2_binary.value = op2

        op1_bits_covered |= op1_binary
        op2_bits_covered |= op2_binary

        set_dut_controls(dut, Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value, op1_binary.value, op2_binary.value)
        await sim_step

        res_bits_covered |= dut.main_res.value

        assert dut.main_res.value == add_uint32_model(op1_binary.value, op2_binary.value)

    raise TestSuccess

@cocotb.test()
async def add_rand_no_overflow_corner(dut):
    """Perform iALU addition test where overflow doesn't happen"""

    op1_bits_covered = BinaryValue(n_bits=32)
    op2_bits_covered = BinaryValue(n_bits=32)
    res_bits_covered = BinaryValue(n_bits=32)

    for _ in range(TEST_ITER_COUNT):

        no_ovflw_res = np.random.randint(0 , 1 << ALU_WIDTH, dtype=np.uint32)
        op1 = np.random.randint(0 , no_ovflw_res - 1, dtype=np.uint32)
        op2 = no_ovflw_res - op1
        # print('op1 = ', hex(op1))
        # print('op2 = ', hex(op2))
        # print('no_ovflw_res = ', hex(no_ovflw_res))

        op1_binary = BinaryValue(n_bits=32)
        op2_binary = BinaryValue(n_bits=32)
        op1_binary.value = op1
        op2_binary.value = op2

        op1_bits_covered |= op1_binary
        op2_bits_covered |= op2_binary

        set_dut_controls(dut, Scr1IaluCmdSelE.SCR1_IALU_CMD_ADD.value, op1_binary.value, op2_binary.value)
        await sim_step

        res_bits_covered |= dut.main_res.value

        assert dut.main_res.value == add_uint32_model(op1_binary.value, op2_binary.value)

    assert op1_bits_covered & op2_bits_covered == (1 << ALU_WIDTH) - 1 , \
    f"only {hex(op1_bits_covered)} {hex(op2_bits_covered)} {hex(res_bits_covered)} bits are covered in this run"

    raise TestSuccess

@cocotb.test()
async def sub_corners_simple(dut):
    """Perform iALU subtract test with min and max op values"""

    corner_vlaues_list = [0x0, 0xFFFF_FFFF]

    for op1 in corner_vlaues_list:
        for op2 in corner_vlaues_list:

            set_dut_controls(dut, Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB.value, op1, op2)
            await sim_step

            assert dut.main_res.value == sub_uint32_model(op1, op2)

    raise TestSuccess

@cocotb.test()
async def sub_rand_underflow_corner(dut):
    """Perform iALU subtract test with negative overflow corner"""

    op1_bits_covered = BinaryValue(n_bits=32)
    op2_bits_covered = BinaryValue(n_bits=32)
    res_bits_covered = BinaryValue(n_bits=32)

    for _ in range(TEST_ITER_COUNT):

        op1 = np.random.randint(0, (1 << ALU_WIDTH) - 1, dtype=np.uint32)
        op2 = np.random.randint(op1, (1 << ALU_WIDTH), dtype=np.uint32)
        # print('op1 = ', hex(op1))
        # print('op2 = ', hex(op2))

        op1_binary = BinaryValue(n_bits=32)
        op2_binary = BinaryValue(n_bits=32)
        op1_binary.value = op1
        op2_binary.value = op2

        op1_bits_covered |= op1_binary
        op2_bits_covered |= op2_binary

        set_dut_controls(dut, Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB.value, op1_binary.value, op2_binary.value)
        await sim_step

        res_bits_covered |= dut.main_res.value

        assert dut.main_res.value == sub_uint32_model(op1_binary.value, op2_binary.value)

    assert op1_bits_covered & op2_bits_covered == (1 << ALU_WIDTH) - 1 , \
    f"only {hex(op1_bits_covered)} {hex(op2_bits_covered)} {hex(res_bits_covered)} bits are covered in this run"

    raise TestSuccess

@cocotb.test()
async def sub_rand_np_underflow_corner(dut):
    """Perform iALU subtract test without negative overflow corner"""

    op1_bits_covered = BinaryValue(n_bits=32)
    op2_bits_covered = BinaryValue(n_bits=32)
    res_bits_covered = BinaryValue(n_bits=32)

    for _ in range(TEST_ITER_COUNT):

        op1 = np.random.randint(0, (1 << ALU_WIDTH), dtype=np.uint32)
        op2 = np.random.randint(0, op1, dtype=np.uint32)
        # print('op1 = ', hex(op1))
        # print('op2 = ', hex(op2))

        op1_binary = BinaryValue(n_bits=32)
        op2_binary = BinaryValue(n_bits=32)
        op1_binary.value = op1
        op2_binary.value = op2

        op1_bits_covered |= op1_binary
        op2_bits_covered |= op2_binary

        set_dut_controls(dut, Scr1IaluCmdSelE.SCR1_IALU_CMD_SUB.value, op1_binary.value, op2_binary.value)
        await sim_step

        res_bits_covered |= dut.main_res.value

        assert dut.main_res.value == sub_uint32_model(op1_binary.value, op2_binary.value)

    assert op1_bits_covered & op2_bits_covered == (1 << ALU_WIDTH) - 1 , \
    f"only {hex(op1_bits_covered)} {hex(op2_bits_covered)} {hex(res_bits_covered)} bits are covered in this run"

    raise TestSuccess
