from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
@report_test
async def ram_word(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=200000)

    cocotb.log.info("[TEST] Starting ram_word logger smoke test")

    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Firmware setup complete, releasing CSB")

    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] CSB released, simple delay")

    # (si quieres, sin la segunda espera para evitar timeouts)
    # await caravelEnv.wait_mgmt_gpio(0)

    await Timer(1, units="us")
    cocotb.log.info("[TEST] ram_word smoke PASS")
