
from ecsm_tool.ecsm_cli.cli_base import CLI_COMMENT

class CLI_NODE(CLI_COMMENT):
    """镜像管理命令"""

    def __init__(self) -> None:
        super().__init__("node", "节点管理")
