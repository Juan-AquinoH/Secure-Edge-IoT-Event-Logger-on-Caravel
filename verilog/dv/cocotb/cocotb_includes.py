import cocotb
from cocotb.triggers import RisingEdge

# Decorador simple para reportar el nombre del test (compatibilidad con caravel_cocotb)
def report_test(func):
    return func

class CaravelEnv:
    def __init__(self, dut):
        self.dut = dut

    async def get_time_clock_trigger(self):
        return self.dut.clk

    # Acceso a registros management por Wishbone mprj (placeholders; ajusta si tienes wrappers reales)
    async def send_management_reg_write(self, addr, data):
        cocotb.log.info(f"MGMT WB WRITE addr=0x{addr:08X} data=0x{data:08X}")

    async def monitor_management_reg_read(self, addr):
        cocotb.log.info(f"MGMT WB READ addr=0x{addr:08X}")
        return 0

    async def monitor_wb_slave_read(self, addr, nbytes):
        cocotb.log.info(f"USER WB READ addr=0x{addr:08X} nbytes={nbytes}")
        return 0

async def test_configure(dut):
    """Configuración mínima del entorno Caravel."""
    cocotb.log.info("test_configure: configuración mínima para secure_logger_test")
    return CaravelEnv(dut)

async def Reset(dut, cycles=5):
    """Reset síncrono simple en rst, si existe."""
    if hasattr(dut, "rst"):
        dut.rst.value = 1
        for _ in range(cycles):
            await RisingEdge(dut.clk)
        dut.rst.value = 0
        for _ in range(cycles):
            await RisingEdge(dut.clk)
    else:
        cocotb.log.warning("Reset: dut.rst no existe, se omite reset")
