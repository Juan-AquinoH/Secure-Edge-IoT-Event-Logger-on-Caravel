from user_proj_tests.ram_word.ram_word import ram_word
from user_proj_tests.secure_test1_asserts.secure_test1_asserts import secure_test1_asserts
from user_proj_tests.secure_test2_asserts.secure_test2_asserts import secure_test2_asserts
from module_trail import secure_logger_la
from user_proj_tests.hello_world.hello_world import hello_world
tests = {
    "RTL-ram_word": {
        "test_module": "user_proj_tests.ram_word.ram_word",
        "testcase": "ram_word",
    },

    "RTL-secure_test1_asserts": {
        "test_module": "user_proj_tests.secure_test1_asserts.secure_test1_asserts",
        "testcase": "secure_test1_asserts",
    },

    "RTL-secure_test2_asserts": {
        "test_module": "user_proj_tests.secure_test2_asserts.secure_test2_asserts",
        "testcase": "secure_test2_asserts",
    },
    "RTL-secure_logger": {
        "test_module": "module_trail",
        "testcase": "secure_logger_la",
    },

    "hello_world": {
        "test_module": "user_proj_tests.hello_world.hello_world",
        "testcase": "hello_world",
    },
    "ram_word": {
        "test_module": "user_proj_tests.ram_word.ram_word",
        "testcase": "ram_word",
    },

}
