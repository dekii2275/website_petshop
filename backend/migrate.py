# backend/migrate.py
import argparse
from typing import Iterable
from contextlib import contextmanager
from sqlalchemy import text
from config import engine

@contextmanager
def connect():
    conn = engine.connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def run_sql(sql: str):
    with connect() as c:
        c.execute(text(sql))

def run_many(sqls: Iterable[str]):
    with connect() as c:
        for s in sqls:
            if s and s.strip():
                c.execute(text(s))

def add_column_if_not_exists(table: str, column: str, col_type: str, extra: str = ""):
    sql = f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type} {extra}".strip()
    run_sql(sql)
    print(f"OK: {table}.{column} ({col_type})")

def create_table_if_not_exists(table: str, columns_ddl: str):
    sql = f"CREATE TABLE IF NOT EXISTS {table} ({columns_ddl})"
    run_sql(sql)
    print(f"OK: table {table}")

def run_sql_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Tách theo dấu chấm phẩy; đơn giản cho DDL
    stmts = [s.strip() for s in content.split(";")]
    run_many(stmts)
    print(f"OK: ran SQL file {path}")

def main():
    parser = argparse.ArgumentParser(description="Simple migration runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sc = sub.add_parser("add-column", help="Add column if not exists")
    sc.add_argument("--table", required=True)
    sc.add_argument("--column", required=True)
    sc.add_argument("--type", required=True, help="SQL type, e.g. DATE, INTEGER, VARCHAR(255)")
    sc.add_argument("--extra", default="", help="Extra DDL, e.g. NOT NULL DEFAULT '2000-01-01'")

    st = sub.add_parser("create-table", help="Create table if not exists")
    st.add_argument("--table", required=True)
    st.add_argument("--columns", required=True, help="Columns DDL inside parentheses")

    sf = sub.add_parser("run-file", help="Run a .sql file")
    sf.add_argument("--path", required=True)

    args = parser.parse_args()
    if args.cmd == "add-column":
        add_column_if_not_exists(args.table, args.column, args.type, args.extra)
    elif args.cmd == "create-table":
        create_table_if_not_exists(args.table, args.columns)
    elif args.cmd == "run-file":
        run_sql_file(args.path)

if __name__ == "__main__":
    main()