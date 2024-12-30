import os
import sqlite3
from abc import ABC
from typing import Optional
from dotenv import load_dotenv
from math import sqrt


class SqliteClient(ABC):
    load_dotenv()
    db_file = os.getenv('PYHURL_SQLITE_DB', 'db.sqlite3')

    @classmethod
    def __get_connection(cls):
        try:
            conn = sqlite3.connect(cls.db_file)
            conn.create_function("sqrt", 1, sqrt)
            return conn
        except sqlite3.OperationalError:
            parent_folder = os.path.dirname(cls.db_file)
            if not os.path.exists(parent_folder):
                os.makedirs(parent_folder)
            conn = sqlite3.connect(cls.db_file)
            conn.create_function("sqrt", 1, sqrt)
            return conn

    @classmethod
    def execute_script(cls, script):
        connection = cls.__get_connection()
        connection.executescript(script)
        connection.commit()
        connection.close()

    @classmethod
    def fetch_many(cls, sql, sql_params=None):
        """
        query db and return all rows
        """
        connection = cls.__get_connection()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        if sql_params:
            rows = cursor.execute(sql, sql_params).fetchall()
        else:
            rows = cursor.execute(sql).fetchall()
        connection.close()
        return rows

    @classmethod
    def fetch_one(cls, sql, sql_params=None):
        """
        query db and return first row
        """
        rows = cls.fetch_many(sql, sql_params)
        return rows[0] if rows else None

    @classmethod
    def fetch_value(cls, sql, sql_params=None):
        """
        query db and return first element of first row
        """
        row = cls.fetch_one(sql, sql_params)
        return row[0] if row else None


    @classmethod
    def insert(cls, sql, params=None) -> Optional[int]:
        """
        insert into db and return last insert id
        """
        connection = cls.__get_connection()
        cursor = connection.cursor()
        cursor.execute("BEGIN;")
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            last_id = cursor.lastrowid
            connection.commit()
        except sqlite3.OperationalError as e:
            connection.rollback()
            raise e
        finally:
            connection.close()
        return last_id

    @classmethod
    def update(cls, sql, params=None) -> int:
        """
        update db and return affected rows
        """
        connection = cls.__get_connection()
        cursor = connection.cursor()
        cursor.execute("BEGIN;")
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            affected_rows = cursor.rowcount
            connection.commit()
        except sqlite3.OperationalError as e:
            connection.rollback()
            raise e
        finally:
            connection.close()
        return affected_rows
