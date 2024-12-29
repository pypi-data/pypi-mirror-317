
import ipaddress

def validate_ip(ip : str):
    """检测输入的 IP 地址是否合法"""
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False

    return True

def ecsm_host_valid(args = None) -> bool:
    if not args:
        return False

    if not getattr(args, "ip", None) or not getattr(args, "port", None):
        print("请输入有效的 ECSM 主机 IP 地址和端口号信息")
        return False

    addr: str = getattr(args, "ip")
    if not validate_ip(addr):
        print("ECSM 主机参数不合法，检测到非法 IP 地址")
        return False

    port: int = int(getattr(args, "port"))
    if port < 100 or port > 65536:
        print("ECSM 主机参数不合法，检测到非法端口号")
        return False

    return True
