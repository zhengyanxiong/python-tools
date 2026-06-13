"""file.cli — pt file <action>"""

import click


def create_cli():
    """文件操作工具（查找、哈希、目录树等）"""

    @click.group(name="file")
    def grp():
        """文件操作工具（查找、哈希、目录树等）"""
        pass

    @grp.command("find")
    @click.argument("directory")
    @click.option("--pattern", "-p", default="*", help="glob 匹配模式")
    @click.option("--max-depth", type=int, default=0, help="最大搜索深度（0=无限制）")
    def find_cmd(directory: str, pattern: str, max_depth: int):
        """查找匹配的文件"""
        from file.core import find_files

        files = find_files(directory, pattern, max_depth)
        for f in files:
            click.echo(f)
        click.echo(f"\n共 {len(files)} 个文件")

    @grp.command("hash")
    @click.argument("file_path")
    @click.option("--algorithm", "-a", default="sha256", help="哈希算法（sha256/md5/sha1）")
    def hash_cmd(file_path: str, algorithm: str):
        """计算文件哈希值"""
        from file.core import file_hash

        result = file_hash(file_path, algorithm)
        click.echo(f"{algorithm}: {result}")

    @grp.command("tree")
    @click.argument("directory")
    @click.option("--max-depth", "-d", type=int, default=3, help="最大显示深度")
    def tree_cmd(directory: str, max_depth: int):
        """显示目录树"""
        from file.core import tree

        click.echo(tree(directory, max_depth))

    return grp
