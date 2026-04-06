#include <firmware_apis.h>

void main()
{
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);

    enableHkSpi(0);
    GPIOs_configureAll(GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_loadConfigs();

    // Avisar al test que la configuración terminó -> wait_mgmt_gpio(1)
    ManagmentGpio_write(1);

    // ... aquí tu transacción WB a la RAM ...

    // Avisar al test que la transacción terminó -> wait_mgmt_gpio(0)
    ManagmentGpio_write(0);

    while (1) {
    }
}

