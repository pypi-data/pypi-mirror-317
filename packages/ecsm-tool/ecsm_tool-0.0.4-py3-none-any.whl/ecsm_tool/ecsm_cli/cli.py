
import argparse
from ecsm_tool.ecsm_cli.cli_base import CLI_COMMENT

class CLI:
    """ECSM 工具集主类"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="ECSM 统一工具集")
        self.subparsers = self.parser.add_subparsers(dest="main", help="ECSM 工具集")
        self.commands: dict[str, CLI_COMMENT] = {}

    def register_command_group(self, command_group: CLI_COMMENT):
        """注册主命令组"""

        command_group.register(self.subparsers)
        self.commands[command_group.name] = command_group

    def run(self) -> None:
        """解析并执行命令"""

        args = self.parser.parse_args()

        if not getattr(args, "main"):
            self.parser.print_help()
            return

        for key, val in self.commands.items():
            if args.main == key and not getattr(args, key):
                val.group_parser.print_help()
                return

        if hasattr(args, "func"):
            args.func(args)
        else:
            print("暂时不支持此功能")
