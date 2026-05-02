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

    # Jerarquía: mprj.secure_top_inst
    secure_top_inst = upw.secure_top_inst
    logger          = secure_top_inst.logger

    # Señales de control de nivel superior
    start_logging = secure_top_inst.start_logging
    power_fail    = secure_top_inst.power_fail_detected
    sensor_data   = secure_top_inst.sensor_data
    aes_key       = secure_top_inst.aes_key

    # Señales de interfaz NVM desde el controlador
    nvm_addr    = logger.nvm_addr
    nvm_data_in = logger.nvm_data_in
    nvm_we      = logger.nvm_we
    done_log    = secure_top_inst.done_logging

    # Inicializa entradas en un estado conocido
    power_fail.value  = 0
    sensor_data.value = 0x3C      # ejemplo de dato de sensor
    aes_key.value     = 0         # clave dummy

    start_logging.value = 0
    await RisingEdge(dut.clock_tb)

    cocotb.log.info("Pulsando start_logging")
    start_logging.value = 1
    await RisingEdge(dut.clock_tb)
    start_logging.value = 0

    write_detected = False

    # Espera a que el logger escriba al menos una vez en la NVM
    for cycle in range(2000):
        await RisingEdge(dut.clock_tb)

        if int(nvm_we.value) == 1:
            cocotb.log.info(
                f"[NVM] Write detected @cycle={cycle}: addr={int(nvm_addr.value)} "
                f"data={int(nvm_data_in.value)}"
            )
            write_detected = True
            break

        if cycle % 100 == 0:
            cocotb.log.info(
                f"[DBG] cycle={cycle} nvm_we={int(nvm_we.value)} "
                f"done_logging={int(done_log.value)}"
            )

    assert write_detected, "No NVM write detected (nvm_we stayed low)"

    cocotb.log.info(">>> TEST OK: secure_logger_la")
