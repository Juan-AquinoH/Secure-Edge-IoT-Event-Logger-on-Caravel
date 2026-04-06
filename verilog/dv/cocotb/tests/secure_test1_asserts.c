#include <firmware_apis.h>   // ajusta al header que tenga tu repo

void main()
{
    // Configura management GPIO como salida y en 0
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);

    enableHkSpi(0);
    GPIOs_configureAll(GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_loadConfigs();

    // Avisar al test: configuración lista -> wait_mgmt_gpio(1)
    ManagmentGpio_write(1);

    // Aquí tu secuencia de Write/Read al logger / ReRam_word
    // ...

    // Avisar al test: secuencia terminada -> wait_mgmt_gpio(0)
    ManagmentGpio_write(0);

    while (1) {
        // loop
    }
}

