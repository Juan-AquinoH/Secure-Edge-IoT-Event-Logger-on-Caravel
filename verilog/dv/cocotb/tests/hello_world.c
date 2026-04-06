#include <defs.h>

void main()
{
    // Firmware mínimo: solo escribe algo en mprj_datal
    reg_mprj_datal = 0x12345678;

    while (1) {
        // loop
    }
}
