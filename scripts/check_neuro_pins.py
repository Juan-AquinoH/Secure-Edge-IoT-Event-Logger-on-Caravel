#!/usr/bin/env python3
import re
from pathlib import Path

lef_file = Path("ip/Neuromorphic_X1_32x32/lef/Neuromorphic_X1_wb.lef")
rtl_file = Path("verilog/rtl/NEUROMORPHIC_X1_stub.v")

lef_pins = set()
with lef_file.open() as f:
    for line in f:
        m = re.match(r"\s*PIN\s+(\S+)", line)
        if m:
            lef_pins.add(m.group(1))

rtl_pins = set()
inside = False
with rtl_file.open() as f:
    for line in f:
        if "module Neuromorphic_X1_wb" in line:
            inside = True
        if inside and ");" in line:
            break
        if inside:
            m = re.match(r"\s*(input|output|inout)\s+(?:wire\s+)?(?:\[[^]]+\]\s+)?(\S+)", line)
            if m:
                name = m.group(2).rstrip(",);")
                rtl_pins.add(name)

print("Pines sólo en LEF:")
for p in sorted(lef_pins - rtl_pins):
    print("  ", p)

print("\nPines sólo en RTL:")
for p in sorted(rtl_pins - lef_pins):
    print("  ", p)
