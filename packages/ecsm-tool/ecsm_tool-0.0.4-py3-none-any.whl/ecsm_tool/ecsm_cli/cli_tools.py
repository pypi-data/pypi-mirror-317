
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
        return False

    port: int = int(getattr(args, "port"))
    if port < 100 or port > 65536:
        return False

    addr: str = getattr(args, "ip")
    if not validate_ip(addr):
        return False

    return True
