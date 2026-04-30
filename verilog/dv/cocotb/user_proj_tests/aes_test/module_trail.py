import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

# =============================
# Driver Wishbone
# =============================
async def wb_write(dut, addr, data):
    dut.wbs_adr_i.value = addr
    dut.wbs_dat_i.value = data
    dut.wbs_we_i.value  = 1
    dut.wbs_stb_i.value = 1
    dut.wbs_cyc_i.value = 1

    await RisingEdge(dut.wb_clk_i)

    while dut.wbs_ack_o.value == 0:
        await RisingEdge(dut.wb_clk_i)

    dut.wbs_stb_i.value = 0
    dut.wbs_cyc_i.value = 0


async def wb_read(dut, addr):
    dut.wbs_adr_i.value = addr
    dut.wbs_we_i.value  = 0
    dut.wbs_stb_i.value = 1
    dut.wbs_cyc_i.value = 1

    await RisingEdge(dut.wb_clk_i)

    while dut.wbs_ack_o.value == 0:
        await RisingEdge(dut.wb_clk_i)

    data = dut.wbs_dat_o.value

    dut.wbs_stb_i.value = 0
    dut.wbs_cyc_i.value = 0

    return data


# =============================
# Test AES
# =============================
@cocotb.test()
async def aes_test(dut):

    dut._log.info("🔥 Starting AES test")

    # Clock real (NO manual toggling)
    clock = Clock(dut.wb_clk_i, 20, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.wb_rst_i.value = 1
    await Timer(100, units="ns")
    dut.wb_rst_i.value = 0

    # =============================
    # Datos AES (vector NIST)
    # =============================
    key = 0x000102030405060708090A0B0C0D0E0F
    plaintext = 0x00112233445566778899AABBCCDDEEFF

    dut._log.info(f"Key: {key:032X}")
    dut._log.info(f"Plaintext: {plaintext:032X}")

    # ⚠️ AJUSTA ESTAS DIRECCIONES A TU WRAPPER
    ADDR_KEY0  = 0x30000000
    ADDR_KEY1  = 0x30000004
    ADDR_KEY2  = 0x30000008
    ADDR_KEY3  = 0x3000000C

    ADDR_TEXT0 = 0x30000010
    ADDR_TEXT1 = 0x30000014
    ADDR_TEXT2 = 0x30000018
    ADDR_TEXT3 = 0x3000001C

    ADDR_CTRL  = 0x30000020
    ADDR_STATUS= 0x30000024

    ADDR_OUT0  = 0x30000030
    ADDR_OUT1  = 0x30000034
    ADDR_OUT2  = 0x30000038
    ADDR_OUT3  = 0x3000003C

    # =============================
    # Escritura clave
    # =============================
    await wb_write(dut, ADDR_KEY0, (key >> 96) & 0xFFFFFFFF)
    await wb_write(dut, ADDR_KEY1, (key >> 64) & 0xFFFFFFFF)
    await wb_write(dut, ADDR_KEY2, (key >> 32) & 0xFFFFFFFF)
    await wb_write(dut, ADDR_KEY3, (key >>  0) & 0xFFFFFFFF)

    # =============================
    # Escritura plaintext
    # =============================
    await wb_write(dut, ADDR_TEXT0, (plaintext >> 96) & 0xFFFFFFFF)
    await wb_write(dut, ADDR_TEXT1, (plaintext >> 64) & 0xFFFFFFFF)
    await wb_write(dut, ADDR_TEXT2, (plaintext >> 32) & 0xFFFFFFFF)
    await wb_write(dut, ADDR_TEXT3, (plaintext >>  0) & 0xFFFFFFFF)

    # Start
    await wb_write(dut, ADDR_CTRL, 0x1)

    # Esperar done (polling)
    done = 0
    for _ in range(100):
        status = await wb_read(dut, ADDR_STATUS)
        if status & 0x1:
            done = 1
            break
        await Timer(100, units="ns")

    assert done, "AES nunca terminó"

    # =============================
    # Leer resultado
    # =============================
    c0 = await wb_read(dut, ADDR_OUT0)
    c1 = await wb_read(dut, ADDR_OUT1)
    c2 = await wb_read(dut, ADDR_OUT2)
    c3 = await wb_read(dut, ADDR_OUT3)

    ciphertext = (int(c0) << 96) | (int(c1) << 64) | (int(c2) << 32) | int(c3)

    expected = 0x69C4E0D86A7B0430D8CDB78070B4C55A

    dut._log.info(f"Ciphertext: {ciphertext:032X}")
    dut._log.info(f"Expected  : {expected:032X}")

    assert ciphertext == expected, "❌ AES incorrecto"

    dut._log.info("✅ AES test PASSED")
