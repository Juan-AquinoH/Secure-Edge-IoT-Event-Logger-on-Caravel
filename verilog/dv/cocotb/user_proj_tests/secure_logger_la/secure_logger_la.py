import cocotb
from caravel_cocotb.caravel_interfaces import test_configure, report_test
from cocotb.triggers import RisingEdge


@cocotb.test()
@report_test
async def secure_logger_la(dut):

    caravelEnv = await test_configure(dut, timeout_cycles=200000)

    caravel   = dut.uut
    chip_core = caravel.chip_core
    upw       = chip_core.mprj

    cocotb.log.info(">>> INICIO secure_logger_la")

    logger = upw.u_secure_top
    nvm    = logger.tmr_nvm

    if hasattr(logger, "start_logging"):
        logger.start_logging.value = 0

    await RisingEdge(dut.clock_tb)

    if hasattr(logger, "start_logging"):
        logger.start_logging.value = 1
        await RisingEdge(dut.clock_tb)
        logger.start_logging.value = 0

    write_detected = False
    read_detected  = False

    for i in range(200):
        await RisingEdge(dut.clock_tb)

        if int(nvm.req_i.value) and int(nvm.we_i.value):
            write_detected = True

        if int(nvm.rvalid_o.value):
            read_detected = True

    assert write_detected, "❌ No hubo escritura en NVM"
    assert read_detected,  "❌ No hubo lectura válida en NVM"

    cocotb.log.info(">>> TEST OK")
