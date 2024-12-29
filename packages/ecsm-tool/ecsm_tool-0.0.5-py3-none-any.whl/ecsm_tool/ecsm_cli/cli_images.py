
from ecsm_tool.ecsm_cli.cli_base import CLI_COMMENT
from ecsm_tool.ecsm_core.repo import ECSM_REPO
import ecsm_tool.ecsm_cli.cli_tools as TOOLS

class CLI_IMAGES(CLI_COMMENT):
    """镜像管理命令"""

    def __init__(self) -> None:
        super().__init__("images", "镜像管理")

        self.add_subcommand(
            name="upload",
            help="镜像上传",
            func=self.upload,
            args=[
                {"flags": ["-i", "--ip"], "options": {"help": "ECSM 服务器 IP 地址", "type": str, "required": True}},
                {"flags": ["-p", "--port"], "options": {"help": "ECSM 服务器端口", "type": str, "required": True}},
                {"flags": ["-f", "--file"], "options": {"help": "目标文件路径", "type": str, "required": True}},
            ],
        )

        self.add_subcommand(
            name="list",
            help="查询镜像列表",
            func=self.list,
            args=[
                {"flags": ["-i", "--ip"], "options": {"help": "ECSM 服务器 IP 地址", "type": str, "required": True}},
                {"flags": ["-p", "--port"], "options": {"help": "ECSM 服务器端口", "type": str, "required": True}},
            ],
        )

        self.add_subcommand(
            name="summary",
            help="查询镜像数量",
            func=self.summary,
            args=[
                {"flags": ["-i", "--ip"], "options": {"help": "ECSM 服务器 IP 地址", "type": str, "required": True}},
                {"flags": ["-p", "--port"], "options": {"help": "ECSM 服务器端口", "type": str, "required": True}},
            ],
        )

    @staticmethod
    def upload(args) -> None:
        if not TOOLS.ecsm_host_valid(args):
            return

        ecsm = ECSM_REPO(args.ip, args.port)
        code, msg  = ecsm.upload_image(args.file, "")
        if code == 0:
            print(f"文件上传成功")
            return

        print(f"上传失败 {msg}")


    @staticmethod
    def list(args) -> None:
        if not TOOLS.ecsm_host_valid(args):
            return

        ecsm = ECSM_REPO(args.ip, args.port)
        code, lists = ecsm.list()
        if code == 0:
            print("ECSM 镜像信息：")
            for item in lists:
                print(f"""
        {item['name']} {item['id']}
    """)


    @staticmethod
    def summary(args) -> None:
        if not TOOLS.ecsm_host_valid(args):
            return

        ecsm = ECSM_REPO(args.ip, args.port)
        code, data = ecsm.summary()
        if code == 0:
            fmt_out = f"""
    ECSM 仓库镜像数量信息：
        本地镜像：{data["local"]}
        远程镜像: {data["remote"]}
    """
            print(fmt_out)
        else:
            print("无法获取有效镜像信息")
