
import sys
import argparse
from ecsm_tool.ecsm_repo import ECSM_REPO

def ecsm_ip_is_valid(args) -> bool:
    if args.ip is None or args.port is None:
        return False

    return True

def ecsm_images_upload(args):
    if not ecsm_ip_is_valid(args):
        return

    ecsm = ECSM_REPO(args.ip, args.port)
    code, msg  = ecsm.upload_image(args.file, "")
    if code == 0:
        print(f"文件上传成功")
        return

    print(f"上传失败 {msg}")

def ecsm_images_list(args):
    if not ecsm_ip_is_valid(args):
        return

    ecsm = ECSM_REPO(args.ip, args.port)
    code, lists = ecsm.list()
    if code == 0:
        print("ECSM 镜像信息：")
        for item in lists:
            print(f"""
    {item['name']} {item['id']}
""")

def ecsm_images_summary(args):
    if not ecsm_ip_is_valid(args):
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


def main():
    parser = argparse.ArgumentParser(description="ECSM 统一工具集")
    subparsers = parser.add_subparsers(dest="main", help="ECSM 子命令")

    # 创建 images 主命令
    images_parser = subparsers.add_parser("images", help="镜像管理")
    images_subparsers = images_parser.add_subparsers(dest="images", help="镜像子命令")

    # 创建 images upload 子命令
    images_upload = images_subparsers.add_parser("upload", help="镜像上传")
    images_upload.add_argument("-i", "--ip",   help="ECSM 服务器 IP 地址", type=str, required=True)
    images_upload.add_argument("-p", "--port", help="ECSM 服务器端口", type=str, required=True)
    images_upload.add_argument("-f", "--file", help="目标文件路径", type=str, required=True)
    images_upload.set_defaults(func=ecsm_images_upload)

    # 创建 images list 子命令
    images_list = images_subparsers.add_parser("list", help="查询镜像列表")
    images_list.add_argument("-i", "--ip",   help="ECSM 服务器 IP 地址", type=str, required=True)
    images_list.add_argument("-p", "--port", help="ECSM 服务器端口", type=str, required=True)
    images_list.set_defaults(func=ecsm_images_list)

    # 创建 images summary 子命令
    images_summary = images_subparsers.add_parser("summary", help="查询镜像数量")
    images_summary.add_argument("-i", "--ip",   help="ECSM 服务器 IP 地址", type=str, required=True)
    images_summary.add_argument("-p", "--port", help="ECSM 服务器端口", type=str, required=True)
    images_summary.set_defaults(func=ecsm_images_summary)

    try:
        args = parser.parse_args()

        if not args.main:
            parser.print_help()
            return

        if args.main == "images" and not args.images:
            images_parser.print_help()
            return

        if hasattr(args, "func"):
            args.func(args)
        else:
            print("暂时不支持此功能")
            return

    except (argparse.ArgumentError, ValueError, SystemExit) as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
