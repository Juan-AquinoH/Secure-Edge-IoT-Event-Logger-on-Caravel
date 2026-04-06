from caravel_cocotb.interfaces.common_functions.test_functions import test_configure, report_test
import cocotb
from cocotb.triggers import RisingEdge

async def wb_write_user(caravelEnv, addr, data):
    """Ciclo WB de escritura al user_project_wrapper."""
    dut = caravelEnv.dut
    mprj = caravelEnv.user_hdl

    mprj.wbs_adr_i.value = addr
    mprj.wbs_dat_i.value = data
    mprj.wbs_we_i.value  = 1
    mprj.wbs_cyc_i.value = 1
    mprj.wbs_stb_i.value = 1

    while True:
        await RisingEdge(caravelEnv.clk)
        if int(mprj.wbs_ack_o.value) == 1:
            break

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
async def secure_logger_la(dut):
    """
    Test básico del logger.
    """
    caravelEnv = await test_configure(dut, timeout_cycles=500000)

    LOGGER_BASE = 0x31000000
    REG_CTRL    = LOGGER_BASE | 0x00
    REG_STATUS  = LOGGER_BASE | 0x04
    REG_DATA0   = LOGGER_BASE | 0x08

    expected_status = 0xDEADBEEF
    expected_data   = 0x00000001

    cocotb.log.info(f"[secure_logger_la] Escribiendo START en 0x{REG_CTRL:08X}")
    await wb_write_user(caravelEnv, REG_CTRL, 0x00000001)

    done = 0
    fail = 0
    max_cycles = 2000

    cocotb.log.info("[secure_logger_la] Iniciando polling de STATUS")
    for i in range(max_cycles):
        status = await wb_read_user(caravelEnv, REG_STATUS)
        done = status & 0x1
        fail = (status >> 1) & 0x1
        data_hw = await wb_read_user(caravelEnv, REG_DATA0)

        cocotb.log.info(
            f"[secure_logger_la] ciclo {i}: "
            f"STATUS=0x{status:08X} (done={done}, fail={fail}) "
            f"DATA0=0x{data_hw:08X}"
        )

        if done or fail:
            cocotb.log.info(
                f"[secure_logger_la] STATUS final=0x{status:08X} en ciclo {i}"
            )

            assert done == 1, "[secure_logger_la] DONE nunca se puso a 1 (timeout)"
            assert fail == 1, "[secure_logger_la] FAIL no se puso a 1 como se esperaba"

            assert status == expected_status, (
                f"[secure_logger_la] STATUS esperado=0x{expected_status:08X}, "
                f"leído=0x{status:08X}"
            )
            assert data_hw == expected_data, (
                f"[secure_logger_la] DATA0 esperado=0x{expected_data:08X}, "
                f"leído=0x{data_hw:08X}"
            )
            break
