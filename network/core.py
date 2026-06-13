"""network.core — 网络工具核心逻辑（占位，按需扩展）"""

import socket


def check_port(host: str, port: int, timeout: float = 3.0) -> dict:
    """检查端口是否可达。"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"host": host, "port": port, "reachable": True}
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        return {"host": host, "port": port, "reachable": False, "error": str(e)}


def dns_lookup(hostname: str) -> dict:
    """DNS 查询。"""
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        ips = list({addr[4][0] for addr in addr_info})
        return {"hostname": hostname, "ips": ips}
    except socket.gaierror as e:
        return {"hostname": hostname, "ips": [], "error": str(e)}
