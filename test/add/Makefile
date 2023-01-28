# Makefile

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(pwd)../../design/scr1_pipe_ialu.sv
TOPLEVEL = scr1_pipe_ialu

MODULE = test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
