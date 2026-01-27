from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb

@cocotb.test()
@report_test
async def ram_word(dut):
    # Setup caravel environment
    caravelEnv = await test_configure(dut, timeout_cycles=200000)

    cocotb.log.info("[TEST] Starting ram_word logger smoke test")

    # Wait until firmware signals setup complete
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Firmware setup complete, releasing CSB")

    # Release chip select so user project can run
    await caravelEnv.release_csb()

    # Wait for firmware to finish test
    await caravelEnv.wait_mgmt_gpio(0)
    cocotb.log.info("[TEST] ram_word single Wishbone transaction completed")
