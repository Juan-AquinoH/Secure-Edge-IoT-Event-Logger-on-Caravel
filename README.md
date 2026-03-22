<p align="center">
  <img src="docs/assets/sponsor_logos_header.png" alt="Perovskia and BM Labs" width="520">
</p>

<p align="center">
  <a href="https://perovskia.solar/"><strong>Perovskia</strong></a> — custom printed perovskite solar cells for harvesting indoor and outdoor light in low-power devices.<br>
  <a href="https://bmsemi.io/"><strong>BM Labs</strong></a> — neuromorphic and ReRAM-focused semiconductor IP for low-power edge and embedded systems.
</p>

# Secure Logger Controller – ReRAM‑Based Medical Event Logger

**ChipFoundry BM Labs NVM Power‑Up Design Contest Submission**  
**Designer:** Juan Carlos Aquino Hernández  
**Institution:** Universidad Tecnológica de Nayarit (UTNAY)  
Designed for the [ChipFoundry BM Labs application challenge](https://chipfoundry.io/challenges/application), this project implements a secure, low‑power medical event logger on the **Caravel** platform.  
It combines BM Labs’ **Neuromorphic ReRAM NVM** with a custom secure logging controller to guarantee data persistence and integrity for critical medical events—even under unexpected power loss.

---

## Project Overview

This repository contains the RTL, integration scripts and documentation for a **Secure Logger Controller** that augments the open‑source [Caravel](https://github.com/efabless/caravel) System‑on‑Chip with non‑volatile event logging.  
The design is targeted at medical wearables and edge devices where power is intermittent and an authenticated audit trail of events is essential.

Key components include:

* **Secure Logger Controller:** Validates, encrypts and writes event payloads to ReRAM.
* **Neuromorphic ReRAM NVM (Neuromorphic_X1):** A non‑volatile memory macro that retains data through power cycles.
* **Caravel Chip Zone:** Provides the Wishbone bus, GPIO and IRQ infrastructure to control and observe the logger.

---

## Key Innovation Points

* **Fail‑safe persistent logging:** sensor events are validated, encrypted and written to non‑volatile memory. Data survives power interruptions.
* **Error detection via CRC‑8:** every event is checked with a CRC‑8 polynomial (0x07). Corrupted events are rejected.
* **Secure writes:** event payloads are encrypted using a 128‑bit AES‑style block (implemented as XOR for simulation) before storage.
* **Tight integration:** the logger, ReRAM macro and Caravel infrastructure share a standard 32‑bit Wishbone bus plus GPIO/IRQ lines for easy verification and tape‑out.

---

## Technical Highlights

| Metric                     | Target / Behaviour                        | Description                                                  |
|---------------------------|-------------------------------------------|--------------------------------------------------------------|
| **Event data width**      | 8‑bit sensor events                      | Simple, low‑bandwidth medical samples or flags.              |
| **Integrity check**       | CRC‑8 (poly 0x07)                        | On‑chip CRC computed before committing an event.             |
| **Encryption block**      | 128‑bit AES‑style block (modeled as XOR) | Event embedded in 128‑bit word and encrypted with a key.     |
| **Power‑failure handling**| Fails closed (fail flag asserted)         | Any power‑fail condition blocks writes and sets an error flag.|
| **Caravel integration**   | Wishbone + GPIO + IRQ                    | Logger controlled via Wishbone and observable via GPIO/IRQ.  |

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/BMsemi/Secure-Edge-IoT-Event-Logger-on-Caravel.git
cd Secure-Edge-IoT-Event-Logger-on-Caravel
```

### 2. Prepare Your Environment

Install the required Caravel harness, management core, OpenLane and SKY130 PDK support:

```bash
make setup
```

### 3. Install ChipFoundry IPM and Neuromorphic X1 IP

```bash
pip install cf-ipm
ipm install Neuromorphic_X1_32x32
```

After installation, replace the behavioural model in the IP directory:

```bash
cd ip/Neuromorphic_X1_32x32
mv hdl hdl_original
mv hdl_replace_inside_ip hdl
# rename supporting folders
mv gdss gds
mv leff lef
mv libb lib
```

### 4. Run Testbenches

Use Cocotb to verify correct operation of the logger controller and ReRAM interface:

```bash
make cocotb-verify-ram_word-rtl
```

### 5. Harden the Design

Generate the physical implementation of the user project wrapper using OpenLane:

```bash
make user_project_wrapper
```

---

## Application Scenarios

### Secure, Fail‑Safe Medical Logging

This IP targets **medical wearables** and **edge sensors** where:

* Power is intermittent (battery‑operated or energy harvesting).
* Events such as heart‑rate anomalies, glucose threshold crossings or respiratory alarms must never be silently lost.
* An encrypted, auditable history of events is required.

It is also suitable for **industrial safety black‑box logging** and **ultra‑low‑power edge monitoring** in harsh environments.

### Secure Logger IP Description

**Secure Logger IP** is an ultra‑low‑power hardware event‑logging core. It guarantees that **critical events are never lost**, preserving data across power failures, resets and communication gaps. Events are captured through an event interface, validated and encrypted, then committed to ReRAM. An NFC interface allows authenticated reads by tapping a phone.

---

## Customer Story: Secure Adherence Cap

The Secure Logger platform can power smart packaging. The **Secure Adherence Cap** looks like a normal cap but behaves like a trusted dose diary. After each use, the cap or dock stores a local event record and later returns a simple phone‑tap view: last dose, adherence history and freshness status.

![Secure Adherence Cap](docs/assets/secure_adherence_cap.png)

**Key value:**

* **Non‑volatile record** survives power interruptions.
* **Validated + encrypted history** available via NFC.
* **Visible perovskite solar insert** functions under cabinet/bathroom light.

---

## Energy Strategy: Perovskite Solar Integration

Intermittent operation is enabled through printed **perovskite solar cells** that conform to caps or wearable patches. Energy is harvested continuously under typical indoor lighting, stored in a thin‑film cell or supercapacitor, and used for short NFC bursts. Stable power rails and a burst buffer ensure reliable operation of the Caravel ASIC and ReRAM macro.

![Perovskite Solar Integration](docs/assets/perovskia_energy_architecture.png)

### Benefits

* Continuous low‑power energy harvesting from indoor light.
* No always‑on wireless required—energy is saved for NFC bursts.
* Maintenance‑free operation optimized for intermittent usage.

---

## Use Case Summary

| Feature                 | Value Delivered             |
|-------------------------|-----------------------------|
| Non‑volatile logging    | No data loss                |
| Secure encryption       | Trusted, auditable records  |
| NFC interface           | Simple user interaction     |
| Energy harvesting ready | Battery independence        |
| Event‑driven design     | Ultra‑low‑power operation   |

---

## Why This Design Wins

* **Innovation:** Combines Neuromorphic ReRAM NVM with a secure logging pipeline—CRC‑8 integrity checks and AES‑style encryption—rather than treating NVM as passive storage.
* **Practicality:** Compact, well‑partitioned architecture that reuses Caravel’s existing bus, GPIO and IRQ infrastructure for control and observability, easing verification and tape‑out integration.
* **Differentiation:** Typical Caravel user projects log or process data in volatile SRAM; this design provides **non‑volatile, integrity‑checked and encrypted event storage**, aligned with safety‑critical medical and edge requirements.

---

## Documentation

* Neuromorphic ReRAM IP: [Neuromorphic X1 documentation](https://github.com/BMsemi/Neuromorphic_X1_32x32)
* Caravel User Project and Wrapper: [Caravel user project docs](https://caravel-user-project.readthedocs.io)
* NVM Power‑Up contest details: [ChipFoundry BM Labs NVM challenge](https://chipfoundry.io/challenges/bmlabs)

---

## License

This project is licensed under the **Apache 2.0** License – see the `LICENSE` file for full terms.