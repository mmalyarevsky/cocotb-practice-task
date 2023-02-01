"""
This module contains behavioral models of 32 bit signed and unsigned integers operations
"""
import numpy as np

def add_uint32_model(op1, op2):
    """returns result of: op1 + op2"""
    uint32_1 = np.array(op1.value).astype(np.uint32)
    uint32_2 = np.array(op2.value).astype(np.uint32)
    return uint32_1 + uint32_2

def sub_uint32_model(op1, op2):
    """returns result of: op1 - op2"""
    uint32_1 = np.array(op1.value).astype(np.uint32)
    uint32_2 = np.array(op2.value).astype(np.uint32)
    return uint32_1 - uint32_2

def sub_lt_int32_model(op1, op2):
    """returns result of signed comparison: op1 < op2"""
    int32_1 = np.array(op1.value).astype(np.int32)
    int32_2 = np.array(op2.value).astype(np.int32)
    if int32_1 < int32_2:
        return 1
    return 0

def sub_ltu_uint32_mode(op1, op2):
    """returns result of unsigned comparison: op1 < op2"""
    uint32_1 = np.array(op1.value).astype(np.uint32)
    uint32_2 = np.array(op2.value).astype(np.uint32)
    if uint32_1 < uint32_2:
        return 1
    return 0
