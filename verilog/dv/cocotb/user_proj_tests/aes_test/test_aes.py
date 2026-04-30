import cocotb
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def aes_test(dut):
    dut._log.info("🔥 Starting AES test")

    # Reset
    dut.wb_rst_i.value = 1
    dut.wb_clk_i.value = 0

    # Generar reloj
    for _ in range(5):
        dut.wb_clk_i.value = 0
        await Timer(10, units="ns")
        dut.wb_clk_i.value = 1
        await Timer(10, units="ns")

    dut.wb_rst_i.value = 0

    # =============================
    # Ejemplo: escribir datos AES
    # =============================

    # Clave AES (128 bits)
    key = 0x000102030405060708090A0B0C0D0E0F

    # Texto plano
    plaintext = 0x00112233445566778899AABBCCDDEEFF

    dut._log.info(f"🔑 Key = {key:032X}")
    dut._log.info(f"📥 Plaintext = {plaintext:032X}")

    # ⚠️ Aquí debes mapear a direcciones reales de tu wrapper
    # Ejemplo:
    # write_reg(dut, ADDR_KEY0, key[31:0])
    # write_reg(dut, ADDR_KEY1, key[63:32])
    # ...

    await Timer(1, units="us")

    # =============================
    # Leer resultado
    # =============================
    # ciphertext = read_reg(...)

    # Valor esperado (vector NIST)
    expected = 0x69C4E0D86A7B0430D8CDB78070B4C55A

    dut._log.info(f"🎯 Expected = {expected:032X}")
    # dut._log.info(f"📤 Cipher = {ciphertext:032X}")

    # assert ciphertext == expected, "AES FAILED"

    dut._log.info("✅ AES test finished")
