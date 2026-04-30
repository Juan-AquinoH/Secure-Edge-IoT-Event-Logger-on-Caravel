# Generic macro fallback grid
define_pdn_grid \
    -macro \
    -default \
    -name macro \
    -starts_with POWER \
    -halo "5 5"

add_pdn_connect \
    -grid macro \
    -layers "met4 met5"

# Neuromorphic macro-specific PDN grid
# Macro placed at [1300.64, 1300.96]
# VDDC pin at ~46.76um from macro origin -> absolute Y ~1347.72um
# offset = 1347.72 mod 180 = 7.72 -> use 7
# This creates stripes at: 7, 187, 367, 547, 727, 907, 1087, 1267, 1447um...
# 1447um is close to VDDC at 1347um - use offset 1347 directly for exact alignment
define_pdn_grid \
    -macro \
    -instances neuro_inst \
    -name neuro_grid \
    -starts_with POWER \
    -halo "5 5"

add_pdn_stripe \
    -grid neuro_grid \
    -layer met3 \
    -width 6 \
    -pitch 180 \
    -offset 1347 \
    -starts_with POWER

add_pdn_connect \
    -grid neuro_grid \
    -layers "met3 met4"
