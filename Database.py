import sqlite3


class Database:
    def __init__(self, db_file_path: str):
        self.con = sqlite3.connect(db_file_path)
        self.cur = self.con.cursor()

    def create_table_if_not_exists(self, table_name: str, columns: str):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.con.commit()

    def insert(self, table_name: str, columns: str, values: str):
        self.cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        self.con.commit()

    def select(self, table_name: str, columns: str, where: str = ""):
        self.cur.execute(f"SELECT {columns} FROM {table_name} {where}")
        return self.cur.fetchall()

    def update(self, table_name: str, new: str, where: str):
        self.cur.execute(f"UPDATE {table_name} SET {new} WHERE {where}")
        self.con.commit()

    def delete(self, table_name: str, where: str):
        self.cur.execute(f"DELETE FROM {table_name} WHERE {where}")
        self.con.commit()

    def user_exists(self, user_id: int) -> bool:
        return bool(self.select("users", "id", f"WHERE id = {user_id}"))
