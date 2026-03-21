Name Project:Secure Logger Controller – ReRAM-Based Medical Event Logger
---
**ChipFoundry BM Labs NVM Power-Up Design Contest Submission**  

**Designer:** Juan Carlos Aquino Hernández

**Institution:** Universidad Tecnológica de Nayarit (UTNAY)

**Contributor:**  Samarth Jainabout  

---

## Project Overview

This project implements a secure, low-power Medical Event Logger SoC on the Caravel platform, integrating BM Labs’ Neuromorphic ReRAM NVM (Neuromorphic_X1) and a custom Secure Logger Controller. The design guarantees data persistence and integrity for critical medical events even under unexpected power loss, enabling robust edge logging in wearable or portable devices.

---
---

## Key Innovation Points

- **Fail-Safe Persistent Logging:** Medical events are validated, encrypted, and safely logged to non-volatile ReRAM, surviving power interruptions.  
- **Error Detection via CRC-8:** A hardware CRC-8 engine validates sensor events before any write, rejecting corrupted data.  
- **Secure Event Writes (AES-style Encryption):** Event payloads are encrypted (AES-style block, currently modeled as AES-XOR for RTL simulation) before being written to NVM.  
- **Caravel + Neuromorphic_X1 Integration:** Fully integrated with Caravel’s user project wrapper and BM Labs’ Neuromorphic_X1_wb macro through a 32-bit Wishbone bus.

---

## Technical Highlights

| Metric                        | Target / Behavior                         | Description                                                  |
|-------------------------------|-------------------------------------------|--------------------------------------------------------------|
| Event Data Width              | 8-bit sensor events                       | Simple, low-bandwidth medical events (vital samples, flags). |
| Integrity Check               | CRC-8 (poly 0x07)                         | On-chip CRC computed for each event before committing.       |
| Encryption Block              | 128-bit AES-style block (modeled as XOR) | Event embedded in 128-bit word and encrypted with key.       |
| Power-Failure Handling        | Fails closed (fail flag asserted)         | Any power_fail condition blocks writes and sets error flag.  |
| Caravel Integration           | Wishbone + GPIO + IRQ                    | Logger controlled via Wishbone and observable via GPIO/IRQ.  |

---

## Architecture
![Arquitectura](https://github.com/user-attachments/assets/5bf1885d-a2a1-470f-8a1d-809667c5cd96)



System-level block diagram showing integration of:

- **Caravel Management SoC (RISC-V core)** providing Wishbone control, debug and system management.  
- **Secure Logger Controller (CRC-8 + AES)** validating sensor events, encrypting payloads, and generating status/IRQ.  
- **Neuromorphic ReRAM NVM (BM Labs Neuromorphic_X1_wb)** used as non-volatile storage and analog in-memory compute macro, connected via 32-bit Wishbone and analog bias pins.

All IPs communicate through the standard **32-bit Wishbone Bus**, with GPIO and Logic Analyzer lines used to inject sensor events, CRC references, power-fail test signals, and to observe encrypted outputs and status flags.

---
1. **Clone the Repository:**

```bash
git clone https://github.com/Juan-AquinoH/secure_logger_controller.git
cd secure_logger_controller

```
---
2. **Prepare Your Environment:**
---

```bash
make setup
```

This installs the Caravel-lite harness, management core, OpenLane, and SKY130 PDK support needed for hardening.

### 3. Install ChipFoundry IPM and Neuromorphic_X1 IP


```bash
pip install cf-ipm
ipm install Neuromorphic_X1_32x32
```

### 4. Install the Neuromorphic X1 IP
```bash
Replace folder hdl inside ip/Neuromorphic_X1_32x32/hdl with folder hdl_replace_inside_ip
Rename hdl_replace_inside_ip inside ip/Neuromorphic_X1_32x32/ with hdl
```

### 5. Edit Behavioral Model Name in IP
```bash
Rename folders
gdss with gds
leff with lef
libb with lib
```

6. **Run Testbenches:**

```bash
make cocotb-verify-ram_word-rtl
```

7. **Harden the Design:**

```bash
make user_project_wrapper
```

---

## Application: Secure, Fail-Safe Medical Logging

This design targets **medical wearables and edge devices** where:

- Power is intermittent (battery-operated, energy harvesting, remote sensors).  
- Event data (heart-rate anomalies, threshold crossings, alarms) must never be silently lost.  
- Security and integrity are mandatory (encrypted event trail with CRC validation).  

It is also suitable for **industrial safety black-box logging** and **ultra-low-power edge monitoring** in harsh environments.
#  Secure Logger IP

##  IP Description

**Secure Logger IP** is an ultra-low-power, hardware-based event logging core designed for medical wearables and edge IoT systems operating under intermittent power and unreliable connectivity.

It guarantees that **critical events are never lost**, preserving data across power failures, resets, and communication gaps.

---

##  Customer Story: Secure Adherence Cap

![Secure Adherence Cap](docs/images/customer_facing_secure_adherence_cap_1.png)
!![secure_logger_customer_story_slide](https://github.com/user-attachments/assets/7fd3dc35-3350-41a3-98a9-f76038e1988c)


A familiar product that looks like a normal cap but behaves like a trusted dose tracker.

After each use:
- A local event is recorded
- Data is stored in non-volatile memory
- No continuous connectivity is required

On user interaction (NFC tap):
- Last dose taken  
- Adherence history  
- Freshness / storage status  

###  Key Value

- Data survives power loss  
- Secure and tamper-proof history  
- No cloud dependency required  

---

##  Final Product Story: Medical Wearable Logger

![Secure Logger ![customer_facing_secure_adherence_cap (4)](https://github.com/user-attachments/assets/82321643-9cea-41cb-ab2f-617b3af30d4b)
!![customer_facing_secure_adherence_cap (4)](https://github.com/user-attachments/assets/f4a2480d-6cf8-4012-881a-b97f233e0e41)


**“The clinical memory inside every patch.”**

Designed for devices where losing data is unacceptable.

The system preserves critical events such as:
- Arrhythmia episodes and symptom markers  
- Glucose threshold crossings and alarms  
- Respiratory deterioration flags  

Even under:
- Low battery  
- Device resets  
- Loss of connectivity  

---

##  Energy Strategy: Perovskite Solar Integration

The device operates in real environments such as:
- Medicine cabinets  
- Bathrooms  
- Indoor lighting conditions  

###  Benefits

- Printed perovskite solar cells conform to caps or wearable patches  
- Continuous low-power energy harvesting  
- Energy stored for short NFC communication bursts  

###  Result

- No always-on wireless required  
- Maintenance-free operation  
- Optimized for intermittent usage patterns  

---

##  IP Architecture

- Event Capture Interface  
- Secure Logging Controller  
- NVM Interface (ReRAM)  
- Cryptographic Validation Unit  
- NFC Communication Interface  
- Power Management Controller  

---

##  Ecosystem & Sponsors

This project is developed within the **BM Labs / ChipFoundry ecosystem**, enabling rapid prototyping of secure, ultra-low-power silicon solutions.

###  BM Labs / ChipFoundry

- Platform for IP-to-silicon innovation  
- Integration into Caravel-based SoCs  
- Focus on NVM and secure edge architectures  
- Supports design, validation, and tapeout readiness  

###  Semiconductor Platform

- Caravel / OpenLane flow  
- Sky130 PDK compatibility  
- RTL-to-GDS implementation  

###  Energy Innovation Layer

- Perovskite solar integration  
- Flexible photovoltaic for wearables  

---

##  Use Case Summary

| Feature                  | Value Delivered              |
|--------------------------|-----------------------------|
| Non-volatile logging     | No data loss                |
| Secure encryption        | Trusted, auditable records  |
| NFC interface            | Simple user interaction     |
| Energy harvesting ready  | Battery independence        |
| Event-driven design      | Ultra-low power operation   |

---

##  Tagline

**Secure Logger IP → Never lose the moment that matters**
---

## Why This Design Wins

**Innovation:**  
Combines BM Labs’ Neuromorphic ReRAM NVM with a secure logging pipeline: CRC-8 integrity checks plus AES-style encryption, rather than treating NVM as just passive storage.

**Practicality:**  
A compact, well-partitioned architecture that reuses Caravel’s existing bus, GPIO, and IRQ infrastructure for control and observability, easing verification and tapeout integration.

**Differentiation:**  
Where typical Caravel user projects log or process data in volatile SRAM, this design provides **non-volatile, integrity-checked and encrypted event storage**, aligned with safety-critical medical and edge requirements.

---

## Documentation

- Neuromorphic ReRAM IP: [Neuromorphic X1 documentation](https://github.com/BMsemi/Neuromorphic_X1_32x32) [web:1]  
- Caravel User Project and Wrapper Requirements: [Caravel User Project docs](https://caravel-user-project.readthedocs.io) [web:5]  
- NVM Power-Up Contest details: [ChipFoundry BM Labs NVM Challenge](https://chipfoundry.io/challenges/bmlabs) [web:6]

---

## License

This project is licensed under the **Apache 2.0** License – see the `LICENSE` file for full terms.
