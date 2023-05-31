from crawler import Patent
from typing import List, Tuple
import random
import sqlite3
from datetime import date

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def get_patents(self, date_from, date_to = date.today(), ipc = None, limit = 50) -> Tuple[int, List[Patent]]:
        # 建立 SQL 查詢的基本語句
        query = f"SELECT * FROM your_table_name WHERE date >= ? AND date <= ? \
            {'AND ipc LIKE ?' if ipc else ''} ORDER BY RANDOM() LIMIT {limit}"

        # 如果提供了ipc(關鍵字)，加入相似性搜尋的條件
        if ipc:
            query += " AND ipc LIKE ?"

        # 執行查詢
        if ipc:
            self.cursor.execute(query, (date_from, date_to, '%' + ipc + '%'))
        else:
            self.cursor.execute(query, (date_from, date_to))

        # 提取查詢結果
        rows = self.cursor.fetchall()

        # 可以進一步處理資料，或返回結果
        return rows
    
    def add_patents(self, patents): ...
    def get_users(self) -> Tuple[str, List[str]]: ...
    def add_users(self, users): ...



