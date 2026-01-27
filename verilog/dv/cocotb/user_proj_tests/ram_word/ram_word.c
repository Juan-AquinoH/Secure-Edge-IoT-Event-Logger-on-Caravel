#define USER_ADDR_SPACE_C_HEADER_FILE

#include <firmware_apis.h>
#include <custom_user_space.h>
#include <stdint.h>

// Simple CPU delay
static inline void wait_cycles(uint32_t cycles)
{
    for (uint32_t i = 0; i < cycles; i++) {
        __asm__ volatile ("nop");
    }
}

#define LOGGER_ADDR 0x31000000
#define NEURO_ADDR 0x30000004
#define NEURO_ADDR_2 0x34000004

uint32_t read_wishbone(uint32_t addr)
{
    return *(volatile uint32_t *)addr;
}

void main()
{
    // --- Basic Caravel setup ---
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);

    GPIOs_configureAll(GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_loadConfigs();

    User_enableIF(1); // enable Wishbone interface

    // Signal cocotb that firmware finished setup
    ManagmentGpio_write(1);

    // ---- SINGLE WISHBONE WRITE ----
    volatile uint32_t addr = LOGGER_ADDR;
    volatile uint32_t addr_neuro = NEURO_ADDR;
    volatile uint32_t addr_neuro_2 = NEURO_ADDR_2;
    volatile uint32_t wdata = 0xC21000FF;
    volatile uint32_t wdata1 = 0x42100000;
    volatile uint32_t wdata_logger = 0x15F34E1F;  // start_logging pulse
    
    // Performing Write Operation
    *((volatile uint32_t *) addr_neuro) = wdata;
    *((volatile uint32_t *) addr_neuro) = wdata1;
    
    wait_cycles(300); // Delay
    
    // // Performing Read Operation
    uint32_t temp = read_wishbone(addr_neuro);
    
    wait_cycles(50); // Delay

    *((volatile uint32_t *)addr) = wdata_logger;
    
    wait_cycles(20); // Delay
    
    *((volatile uint32_t *)addr) = 0x1234567F;
    
    wait_cycles(20); // Delay
    
    *((volatile uint32_t *)addr) = 0x15F34E14;

    // small delay to let hardware react
    wait_cycles(200);

    // Optional: read back (not needed, but included for reference)
    volatile uint32_t status = read_wishbone(addr);

    // Test finished
    ManagmentGpio_write(0);

    while(1); // stop CPU
}
