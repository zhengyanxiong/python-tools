"""network.cli — pt network <action>"""

import click


def create_cli():
    """网络工具（端口检查、DNS 查询等）"""

    @click.group(name="network")
    def grp():
        """网络工具（端口检查、DNS 查询等）"""
        pass

    @grp.command("check-port")
    @click.argument("host")
    @click.argument("port", type=int)
    @click.option("--timeout", default=3.0, help="超时秒数")
    def check_port_cmd(host: str, port: int, timeout: float):
        """检查端口是否可达"""
        from network.core import check_port

        result = check_port(host, port, timeout)
        status = "✅ 可达" if result["reachable"] else "❌ 不可达"
        click.echo(f"{host}:{port} — {status}")
        if not result["reachable"]:
            click.echo(f"  原因: {result.get('error', 'unknown')}")

    @grp.command("dns")
    @click.argument("hostname")
    def dns_cmd(hostname: str):
        """DNS 查询"""
        from network.core import dns_lookup

        result = dns_lookup(hostname)
        if result["ips"]:
            click.echo(f"{hostname} → {', '.join(result['ips'])}")
        else:
            click.echo(f"❌ 解析失败: {result.get('error', 'unknown')}")

    return grp
