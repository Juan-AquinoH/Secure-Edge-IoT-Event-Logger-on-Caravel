#include <defs.h>
#include <stub.c>

// Test dummy: solo arranca el SoC y deja que cocotb controle todo.
void main()
{
    // Enable wishbone & la, etc. según tu proyecto; para dummy basta:
    reg_mprj_io_0 = GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);

    // Señal simple para saber que el programa arrancó
    reg_mprj_datal = 0xA5A5A5A5;

    // Loop infinito; cocotb maneja el resto.
    while (1);
}
