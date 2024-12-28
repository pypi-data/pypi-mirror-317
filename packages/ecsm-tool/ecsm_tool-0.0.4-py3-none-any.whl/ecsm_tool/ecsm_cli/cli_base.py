
from typing import Callable
import argparse

class CLI_COMMENT:
    """基础公共命令集"""

    def __init__(self, name: str, help_desc: str) -> None:
        self.name: str = name
        self.help: str = help_desc
        self.subcommands: list = []
        self.group_parser: argparse.ArgumentParser
        self.checkers: list[Callable] = []

    def add_subcommand(self, name: str, help: str, func, args: list[dict] | None) -> None:
        """添加子命令"""

        self.subcommands.append({
            "name": name,
            "help": help,
            "func": func,
            "args": args or [],
        })

    def add_checker(self, func: Callable) -> bool:
        self.checkers.append(func)
        return True

    def register(self, subparsers):
        """注册子命令到主命令解析器"""

        self.group_parser = subparsers.add_parser(self.name, help=self.help)
        group_subparsers = self.group_parser.add_subparsers(dest=self.name, help=f"{self.name} 子命令")
        for subcommand in self.subcommands:
            sub_parser = group_subparsers.add_parser(subcommand["name"], help=subcommand["help"])
            for arg in subcommand["args"]:
                sub_parser.add_argument(*arg["flags"], **arg["options"])
            sub_parser.set_defaults(func=subcommand["func"])
