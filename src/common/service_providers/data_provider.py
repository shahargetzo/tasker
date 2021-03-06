import time
import typing
from dataclasses import dataclass

import mysql.connector

from src.common.tasker_logger import Logger
from src.common.utils import sql_utils

key_updated_at = 'updated_at'

config = {
    'user': 'root',
    'password': 'root',
    'port': '3306',
    'database': 'tasker',
    'host': 'db'
}


@dataclass
class DBWhere:
    field: str
    operation: str
    value: 'typing.Any'


class DataProvider:
    def __init__(self, logger):
        self.logger: Logger = logger
        self.connection = None

    def execute_with_data(self, sql: str, values: tuple) -> int:
        self.logger.debug(f'executing {sql} with values {values}')
        cursor = self.get_cursor()
        cursor.execute(sql, values)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        rowcount = cursor.rowcount
        self.logger.debug(f'rowcount: {rowcount}')
        return rowcount

    def insert(self, table_name: str, keys: list, values: tuple) -> bool:
        if len(keys) != len(values):
            raise Exception(f'keys and value must have equal len. keys: {keys}, values: {values}')
        if len(set(keys)) != len(keys):
            raise Exception(f'some keys appears twice in this query: {keys}')
        values_format = '%s,' * len(values)
        values_format = values_format[:-1]
        fields = ",".join(keys)
        sql = f'INSERT INTO {table_name} ({fields}) VALUES ({values_format})'
        rowcount = self.execute_with_data(sql, values)
        return True if rowcount == 1 else False

    def execute(self, sql):
        cursor = self.get_cursor()
        cursor.execute(sql)
        cursor.fetchall()
        self.connection.commit()
        cursor.close()

    def get_cursor(self, buffered=False):
        self.close_connection()
        self.create_connection()
        # if self.connection is None or not self.connection.is_connected():
        #     self.create_connection()
        if buffered:
            return self.connection.cursor(buffered=True, dictionary=True)
        return self.connection.cursor()

    def update_row(self, table_name: str, to_update: dict, where: list):
        sql = f'update {table_name} set {key_updated_at}={int(round(time.time()))}'
        for key_to_update in to_update:
            sql += f', {key_to_update}="{to_update[key_to_update]}" '
        if where:
            sql += ' where '
            for w in where:
                sql += f' {w}="{where[w]}" and'
                # update_values.append(where[w])
            sql = sql[:-len('and')]
        return self.execute(sql)

    def get_rows(self, table_name: str, where: list = None, limit: int = None, fields: list = None,
                 index: str = None) -> list:
        sql = 'select '
        if fields:
            sql += ','.join(fields)
        else:
            sql += ' *'
        sql += f' from {table_name} '
        if index:
            sql += f' use index ({index}) '
        if where:
            sql += f' WHERE '
            for i, w in enumerate(where):
                assert isinstance(w, DBWhere)
                sql += f'{w.field} {w.operation} {sql_utils.get_field_val_for_query(w.value)}'
                if i < len(where) - 1:
                    sql += ' and '
        if limit:
            sql += f' limit {limit}'
        cursor = self.get_cursor()
        self.logger.debug(f'executing {sql}')
        try:
            cursor.execute(sql)
        except Exception as e:
            raise Exception(f'got exception while executing {sql}: {e}')
        db_records = cursor.fetchall()
        # db_records = self.get_cursor(buffered=True).fetchall()
        ret_records = []
        for rec in db_records:
            ret_rec = {}
            i = 0
            for col in cursor.column_names:
                ret_rec[col] = rec[i]
                i += 1
            ret_records.append(ret_rec)
        self.connection.commit()
        cursor.close()
        return ret_records

    def create_connection(self):
        if self.connection is None:
            try:
                self.logger.debug(f'creating connection with config {config}')
                self.connection = mysql.connector.connect(**config)
            except Exception as e:
                self.logger.error(f'failed to connect to db. error: {str(e)}, config: {config}')
                raise

    def close_connection(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception as e:
                self.logger.error(f'failed to close connection: {str(e)}')
            self.connection = None
