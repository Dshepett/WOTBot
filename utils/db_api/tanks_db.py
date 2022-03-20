import sqlite3
import pandas as pd


class Database:
    def __init__(self, path_to_db="tanks.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def excecute(self, sql, parameters=None, fetchone=False, fetchall=False, commit=False):
        data = None
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_tanks(self, path="tanks.csv"):
        self.excecute("DROP TABLE IF EXISTS Tanks;")
        data = pd.read_csv(path, sep=";")
        data.to_sql('Tanks',self.connection, index=False)


    def find_tank(self, data):
        sql = """
        SELECT * FROM Tanks WHERE
        Health > ? - 200 AND Health < ? + 200
        AND Damage > ? - 200 AND Damage < ? + 200
        AND Armor > ? - 35 AND Armor < ? + 35
        AND Speed > ? - 15 AND Speed < ? + 15
        AND Stealth > ? - 10 AND Stealth < ? + 10
        """
        return self.excecute(sql, data, fetchall=True)            
