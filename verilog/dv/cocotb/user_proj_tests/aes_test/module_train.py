# ============================================================
# module_trail.py
# Cocotb entrypoint wrapper (CF / Caravel verification flow)
# ============================================================

import cocotb

# IMPORTANTE:
# Solo se importa el módulo del test.
# Cocotb detecta automáticamente @cocotb.test()

import user_proj_tests.test_aes.test_aes  # AES test

# ------------------------------------------------------------
# Si CF ejecuta otros tests, aquí se agregan también:
# ------------------------------------------------------------

# import user_proj_tests.hello_world.hello_world
# import user_proj_tests.ram_word.ram_word
# import user_proj_tests.secure_test1_asserts.secure_test1_asserts
# import user_proj_tests.secure_test2_asserts.secure_test2_asserts

# ============================================================
# NOTA IMPORTANTE:
# NO se llaman funciones manualmente.
# NO usar test_aes()
# Cocotb lo registra vía @cocotb.test()
# ============================================================
