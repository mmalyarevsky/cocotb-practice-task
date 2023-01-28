# Makefile

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

PWD = $(shell pwd)

export PYTHONPATH := $(PWD)/include:$(PYTHONPATH)

VERILOG_SOURCES += $(PWD)/../design/scr1_pipe_ialu.sv
TOPLEVEL = scr1_pipe_ialu

MODULE = test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
