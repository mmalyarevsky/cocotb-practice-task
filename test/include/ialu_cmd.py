"""
Enums for available iALU commands
"""
from enum import Enum

class Scr1IaluCmdSelE(Enum):
    """available scr1 ialu cmds"""
    SCR1_IALU_CMD_NONE     = 0  # IALU disable
    SCR1_IALU_CMD_AND      = 1  # op1 & op2
    SCR1_IALU_CMD_OR       = 2  # op1 | op2
    SCR1_IALU_CMD_XOR      = 3  # op1 ^ op2
    SCR1_IALU_CMD_ADD      = 4  # op1 + op2
    SCR1_IALU_CMD_SUB      = 5  # op1 - op2
    SCR1_IALU_CMD_SUB_LT   = 6  # op1 < op2
    SCR1_IALU_CMD_SUB_LTU  = 7  # op1 u< op2
    SCR1_IALU_CMD_SUB_EQ   = 8  # op1 = op2
    SCR1_IALU_CMD_SUB_NE   = 9  # op1 != op2
    SCR1_IALU_CMD_SUB_GE   = 10 # op1 >= op2
    SCR1_IALU_CMD_SUB_GEU  = 11 # op1 u>= op2
    SCR1_IALU_CMD_SLL      = 12 # op1 << op2
    SCR1_IALU_CMD_SRL      = 13 # op1 >> op2
    SCR1_IALU_CMD_SRA      = 14 # op1 >>> op2