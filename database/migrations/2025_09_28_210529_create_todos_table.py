"""
Migration: create_todos_table
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, TIMESTAMP
from datetime import datetime

class Migration:
    def up(self, engine):
        meta = MetaData()
        Table(
            "todos", meta,
            Column("id", Integer, primary_key=True),
            Column("name", String(255)),
            Column("created_at", TIMESTAMP, default=datetime.utcnow),
        )
        meta.create_all(engine)
        print("🔼 Creating table: todos")

    def down(self, engine):
        meta = MetaData(bind=engine)
        table = Table("todos", meta, autoload_with=engine)
        table.drop(engine)
        print("🔽 Dropping table: todos")
