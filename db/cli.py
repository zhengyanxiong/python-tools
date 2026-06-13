"""db.cli — pt db <action>"""

import click

from common.deps import require


def create_cli():
    """数据库工具（ER 图生成等）"""

    @click.group(name="db")
    def grp():
        """数据库工具（ER 图生成等）"""
        pass

    @grp.command("er-diagram")
    @click.option("--host", default="localhost", help="数据库主机")
    @click.option("--port", default="5432", help="数据库端口")
    @click.option("--dbname", required=True, help="数据库名称")
    @click.option("--user", default="root", help="数据库用户")
    @click.option("--password", default="", help="数据库密码")
    @click.option("--output", "-o", default="er_diagram.png", help="输出图片路径")
    def er_diagram_cmd(host, port, dbname, user, password, output):
        """连接数据库，提取表结构，推断外键关系，生成 ER 图"""
        require("psycopg2", "db", hint="pip install -r requirements/db.txt")
        require("sqlalchemy", "db", hint="pip install -r requirements/db.txt")
        require("eralchemy", "db", hint="pip install -r requirements/db.txt")

        import psycopg2
        from db.core import generate_er_diagram, get_table_structures, infer_relationships

        try:
            conn = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password
            )
        except Exception as e:
            click.echo(f"❌ 数据库连接失败: {e}", err=True)
            raise SystemExit(1)

        try:
            structures = get_table_structures(conn)
            relationships = infer_relationships(structures)
            result_path = generate_er_diagram(structures, relationships, output)
            click.echo(f"✅ ER 图已生成: {result_path}")
        finally:
            conn.close()

    return grp
