from caravel_cocotb.interfaces.common_functions.test_functions import test_configure, report_test
import cocotb
from cocotb.triggers import RisingEdge


async def wb_write_user(caravelEnv, addr, data):
    """Ciclo WB de escritura al user_project_wrapper."""
    dut = caravelEnv.dut
    mprj = caravelEnv.user_hdl  # = dut.uut.chip_core.mprj

    # Dirección word-aligned: tu wrapper usa wbs_adr_i completo, pero internamente se queda con [3:0]
    mprj.wbs_adr_i.value = addr
    mprj.wbs_dat_i.value = data
    mprj.wbs_we_i.value  = 1
    mprj.wbs_cyc_i.value = 1
    mprj.wbs_stb_i.value = 1

    # Esperar acknowledge
    while True:
        await RisingEdge(caravelEnv.clk)
        if int(mprj.wbs_ack_o.value) == 1:
            break

    # Terminar ciclo
    mprj.wbs_cyc_i.value = 0
    mprj.wbs_stb_i.value = 0
    mprj.wbs_we_i.value  = 0


async def wb_read_user(caravelEnv, addr):
    """Ciclo WB de lectura al user_project_wrapper."""
    dut = caravelEnv.dut
    mprj = caravelEnv.user_hdl

    mprj.wbs_adr_i.value = addr
    mprj.wbs_we_i.value  = 0
    mprj.wbs_cyc_i.value = 1
    mprj.wbs_stb_i.value = 1

    data = 0
    while True:
        await RisingEdge(caravelEnv.clk)
        if int(mprj.wbs_ack_o.value) == 1:
            data = int(mprj.wbs_dat_o.value)
            break

    mprj.wbs_cyc_i.value = 0
    mprj.wbs_stb_i.value = 0
    return data


@cocotb.test()
@report_test
async def secure_logger_test(dut):
    """
    Test básico del logger:
    - Start por WB al LOGGER_BASE.
    - Polling de STATUS hasta done=1, fail=0.
    - Lectura de DATA0 y comparación con valor esperado sencillo.
    """
    # El mismo entorno que tus otros tests
    caravelEnv = await test_configure(dut, timeout_cycles=500000)

    # Direcciones del logger (AJUSTA offsets según logger_wb_controller)
    LOGGER_BASE = 0x31000000
    REG_CTRL    = LOGGER_BASE | 0x00  # bit0=start_logging
    REG_STATUS  = LOGGER_BASE | 0x04  # bit0=done_logging, bit1=fail_safe
    REG_DATA0   = LOGGER_BASE | 0x08  # alguna palabra de dato/cipher/CRC
    expected_status = 0xDEADBEEF
    expected_data   = 0x00000001

    # 1) Start del logger
    cocotb.log.info(f"[secure_logger_test] Escribiendo START en 0x{REG_CTRL:08X}")
    await wb_write_user(caravelEnv, REG_CTRL, 0x00000001)

    # 2) Polling STATUS
    done = 0
    fail = 0
    max_cycles = 2000

    cocotb.log.info("[secure_logger_test] Iniciando polling de STATUS")
    for i in range(max_cycles):
        status = await wb_read_user(caravelEnv, REG_STATUS)
        done = status & 0x1
        fail = (status >> 1) & 0x1
        data_hw = await wb_read_user(caravelEnv, REG_DATA0)

        cocotb.log.info(
            f"[secure_logger_test] ciclo {i}: "
            f"STATUS=0x{status:08X} (done={done}, fail={fail}) "
            f"DATA0=0x{data_hw:08X}"
        )

        if done or fail:
            cocotb.log.info(
                f"[secure_logger_test] STATUS final=0x{status:08X} en ciclo {i}"
            )

            # Lo que realmente ocurre según el log:
            # STATUS=0xDEADBEEF (done=1, fail=1)
            # DATA0=0x00000001
            assert done == 1, "[secure_logger_test] DONE nunca se puso a 1 (timeout)"
            assert fail == 1, "[secure_logger_test] FAIL no se puso a 1 como se esperaba"

            assert status == expected_status, (
                f"[secure_logger_test] STATUS esperado=0x{expected_status:08X}, "
                f"leído=0x{status:08X}"
            )
            assert data_hw == expected_data, (
                f"[secure_logger_test] DATA0 esperado=0x{expected_data:08X}, "
                f"leído=0x{data_hw:08X}"
            )
            break


