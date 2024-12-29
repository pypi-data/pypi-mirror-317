
from ecsm_tool.ecsm_cli.cli_tools import ecsm_host_valid

class TEST_ARGS:
    def __init__(self) -> None:
        pass

def test_checker():
    tcase_0 = TEST_ARGS()
    setattr(tcase_0, "ip", "10.9.0.10")
    setattr(tcase_0, "port", 3001)

    tcase_1 = TEST_ARGS()
    setattr(tcase_1, "ip", 3001)

    assert ecsm_host_valid(None) == False
    assert ecsm_host_valid(tcase_0) == True
    assert ecsm_host_valid(tcase_1) == False
