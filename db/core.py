"""db.core — 数据库工具核心逻辑（无 CLI 依赖，可独立 import）"""

import re
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table, text


def get_table_structures(connection) -> dict[str, list[tuple]]:
    """通过 psycopg2 连接获取指定 schema 下的表结构。

    Args:
        connection: psycopg2 连接对象
        schema: 数据库 schema 名（默认 'public'）

    Returns:
        {table_name: [(column_name, data_type), ...]}
    """
    cursor = connection.cursor()
    cursor.execute(
        """SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'"""
    )
    tables = [row[0] for row in cursor.fetchall()]

    table_structures: dict[str, list[tuple]] = {}
    for table_name in tables:
        cursor.execute(
            """SELECT column_name, data_type
               FROM information_schema.columns
               WHERE table_name = %s""",
            (table_name,),
        )
        table_structures[table_name] = cursor.fetchall()

    return table_structures


def infer_relationships(table_structures: dict[str, list[tuple]]) -> list[tuple]:
    """推断表间关系：查找以 _id 结尾的列并关联对应表。

    Returns:
        [(source_table, column_name, target_table, target_column), ...]
    """
    relationships = []
    for table, columns in table_structures.items():
        for col_name, _ in columns:
            if re.search(r"_id$", col_name):
                target_table = col_name.replace("_id", "")
                if target_table in table_structures:
                    relationships.append((table, col_name, target_table, "id"))
    return relationships


def generate_er_diagram(
    table_structures: dict[str, list[tuple]],
    relationships: list[tuple],
    output_path: str = "er_diagram.png",
) -> str:
    """根据表结构和关系生成 ER 图。

    Args:
        table_structures: {table_name: [(col_name, data_type), ...]}
        relationships: [(src_table, col, tgt_table, tgt_col), ...]
        output_path: 输出图片路径

    Returns:
        输出文件的绝对路径
    """
    from eralchemy import render_er

    metadata = MetaData()
    tables: dict[str, Table] = {}

    for table_name, columns in table_structures.items():
        cols = [
            Column(col_name, Integer, primary_key=(col_name == "id"))
            for col_name, _ in columns
        ]
        tables[table_name] = Table(table_name, metadata, *cols)

    for src_table, col, tgt_table, tgt_col in relationships:
        if src_table in tables and tgt_table in tables:
            fk = ForeignKey(f"{tgt_table}.{tgt_col}")
            tables[src_table].append_column(Column(col, Integer, fk))

    engine = sa.create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    render_er(metadata, output_path)

    return str(Path(output_path).resolve())
