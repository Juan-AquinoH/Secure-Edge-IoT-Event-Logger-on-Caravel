import cocotb
from caravel_cocotb.caravel_interfaces import test_configure, report_test

@cocotb.test()
@report_test
async def hello_world(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=500000)
    cocotb.log.info("[TEST] Hello World from Caravel cocotb")
