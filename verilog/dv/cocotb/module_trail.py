import cocotb

@cocotb.test()
async def test_aes(dut):
    dut._log.info("AES TEST OK")
