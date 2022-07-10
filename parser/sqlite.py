import logging
import sqlite3


class Database:
    def __init__(self, path_to_db='./data/gold.db'):
        self.path_to_db = path_to_db

    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        connection = self.connection()
        connection.set_trace_callback(logger)
        if not parameters:
            parameters = tuple()
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table(self):
        sql2 = """
        CREATE TABLE history(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            datetime varchar(255) NOT NULL,
            dealer varchar(255) NOT NULL,
            buy varchar(255),
            sell varchar(255)
        );
        """
        self.execute(sql2, commit=True)

    def add_history(self, datetime:str, dealer:str, buy:float, sell:float):
        sql = "INSERT INTO history(datetime, dealer, buy, sell) VALUES (?,?,?,?)"
        parameters = (datetime, dealer, buy, sell)
        self.execute(sql, parameters=parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters

        ])
        return sql, tuple(parameters.values())

def logger(statement):
    print(f'''
________________________________
Executing:
{statement}
________________________________
''')
