TOPLEVEL_LANG = verilog

# RTL del diseño
VERILOG_SOURCES += $(CARAVEL_ROOT)/verilog/rtl/caravel.v
VERILOG_SOURCES += $(CARAVEL_ROOT)/verilog/rtl/user_project_wrapper.v

# Test cocotb
MODULE = secure_logger_la
TOPLEVEL = user_project_wrapper

# Runner de Caravel
include $(CARAVEL_ROOT)/verilog/dv/cocotb/caravel.mk
