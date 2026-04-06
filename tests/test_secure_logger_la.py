import cocotb
from caravel_cocotb.caravel_interfaces import test_configure, report_test
from cocotb.triggers import RisingEdge


@cocotb.test()
@report_test
async def secure_logger_la(dut):

    # Inicializa Caravel (firmware + reset)
    caravelEnv = await test_configure(dut, timeout_cycles=200000)

    caravel   = dut.uut
    chip_core = caravel.chip_core
    upw       = chip_core.mprj

    cocotb.log.info(">>> INICIO secure_logger_la")

    # Instancias (ajusta nombres si cambian)
    logger = upw.u_secure_top
    nvm    = logger.tmr_nvm

    # -------------------------------
    # 1. Estado inicial
    # -------------------------------
    if hasattr(logger, "start_logging"):
        logger.start_logging.value = 0

    await RisingEdge(dut.clock_tb)

    # -------------------------------
    # 2. Generar evento
    # -------------------------------
    if hasattr(logger, "start_logging"):
        logger.start_logging.value = 1
        await RisingEdge(dut.clock_tb)
        logger.start_logging.value = 0

    cocotb.log.info(">>> Evento disparado")

    # -------------------------------
    # 3. Monitoreo NVM
    # -------------------------------
    write_detected = False
    read_detected  = False

    for i in range(200):
        await RisingEdge(dut.clock_tb)

        req    = int(nvm.req_i.value)
        we     = int(nvm.we_i.value)
        rvalid = int(nvm.rvalid_o.value)

        if req and we:
            write_detected = True

        if rvalid:
            read_detected = True

    # -------------------------------
    # 4. ASSERTS (clave)
    # -------------------------------
    assert write_detected, "❌ No hubo escritura en NVM"
    assert read_detected,  "❌ No hubo lectura válida en NVM"

    cocotb.log.info(">>> TEST OK: NVM activa")
