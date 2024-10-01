import re

import psycopg2
import sqlalchemy as sa
from eralchemy import render_er
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, text

# 配置数据库连接
db_config = {
    'dbname': 'bernie',
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'port': '5432'
}


# 连接到数据库
def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


# 提取表的字段和推断关系
def get_table_structures(connection):
    try:
        cursor = connection.cursor()

        # 获取所有表名
        cursor.execute("""SELECT table_name FROM information_schema.tables
                          WHERE table_schema = 'test'""")
        tables = cursor.fetchall()

        table_structures = {}

        # 获取每个表的列信息
        for table in tables:
            table_name = table[0]
            cursor.execute(f"""SELECT column_name, data_type
                               FROM information_schema.columns
                               WHERE table_name = '{table_name}'""")
            columns = cursor.fetchall()
            table_structures[table_name] = columns

        return table_structures

    except Exception as e:
        print(f"Error retrieving table structures: {e}")
        return {}


# 推断字段关联
def infer_relationships(table_structures):
    relationships = []

    # 简单的推断方法：寻找列名中包含 '_id' 的列，并将其与其他表中的主键（假设为 id）关联
    for table, columns in table_structures.items():
        for column in columns:
            column_name = column[0]
            if re.search(r'_id$', column_name):
                # 尝试推断关联到的表名
                related_table = column_name.replace('_id', '')
                table_structures[table].remove(column)
                if related_table in table_structures:
                    relationships.append((table, column_name, related_table, 'id'))

    return relationships


# 手动创建关联并生成 ER 图
def generate_er_diagram(relationships):
    metadata = MetaData()

    tables = {}

    # 创建表结构（假设所有表的主键都是 'id'，可以根据实际情况调整）
    for table, columns in table_structures.items():
        columns_list = [Column(col[0], Integer, primary_key=(col[0] == 'id')) for col in columns]
        tables[table] = Table(table, metadata, *columns_list)

    # 根据推断的关系添加外键
    for table, column, related_table, related_column in relationships:
        if table in tables and related_table in tables:
            fk = ForeignKey(f"{related_table}.{related_column}")
            tables[table].append_column(Column(column, Integer, fk))

    # ss
    # 使用 ERAlchemy 生成 ER 图
    try:
        engine = sa.create_engine('sqlite:///:memory:')
        with engine.connect() as sql_con:
            metadata.drop_all(engine)
            metadata.create_all(engine)
            # 查询内存数据库中的所有表
            result = sql_con.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            # 获取并打印所有表名
            tables_in_memory = result.fetchall()
            print("Tables in memory database:", tables_in_memory)
            # 查看某个表的结构 (以 'student' 表为例)
            table_name = 'student'
            result = sql_con.execute(text(f"PRAGMA table_info({table_name});"))

            print(f"Structure of table '{table_name}':")
            columns_info = result.fetchall()
            for col in columns_info:
                print(col)

        render_er(metadata, 'er_diagram_with_inferred_relationships.png')
        print(
            "ER diagram with inferred relationships generated successfully and saved as 'er_diagram_with_inferred_relationships.png'")
    except Exception as e:
        print(f"Error generating ER diagram: {e}")


if __name__ == '__main__':
    connection = connect_to_db()
    if connection:
        table_structures = get_table_structures(connection)
        relationships = infer_relationships(table_structures)
        generate_er_diagram(relationships)
        connection.close()
