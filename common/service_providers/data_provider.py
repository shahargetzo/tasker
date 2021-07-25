import mysql.connector
import time

key_updated_at = 'updated_at'

config = {
    'user': 'root',
    'password': 'root',
    'port': '3306',
    # 'port': '32000',
    'database': 'tasker',
    'host': 'db'
}


class DataProvider:
    def __init__(self, logger):
        self.logger = logger
        self.connection = None

    def execute_with_data(self, sql: str, values: tuple) -> int:
        cursor = self.get_cursor()
        self.logger.debug(f'executing {sql} with values {values}')
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
        cursor.close()

    def fetch_all(self):
        cursor = self.get_cursor
        fetch = cursor(buffered=True).fetchall()
        cursor().close()
        return fetch

    def get_cursor(self, buffered=False):
        if self.connection is None:
            self.create_connection()
        if buffered:
            return self.connection.cursor(buffered=True, dictionary=True)
        return self.connection.cursor()

    def execute_and_fetch_all(self, sql):
        cursor = self.get_cursor()
        cursor.execute(sql)
        fetch = cursor.fetchall()
        cursor.close()
        return fetch

    def update_row(self, table_name: str, to_update: dict, where: list):
        sql = f'update {table_name} set {key_updated_at}={int(round(time.time()))}'
        update_values = []
        for key_to_update in to_update:
            sql += f', {key_to_update}="%s" '
            update_values.append(to_update[key_to_update])
        if where:
            sql += ' where '
            for w in where:
                sql += f' {w}="%s" and'
                update_values.append(where[w])
            sql = sql[:len('and')]
        return self.execute_with_data(sql, tuple(update_values))

    def get_rows(self, table_name: str, where: list, limit: int = 0, fields: list = None) -> list:
        sql = 'select '
        if fields:
            sql += ','.join(fields)
        else:
            sql += ' *'
        sql += f' from {table_name} '
        if where:
            sql += f' WHERE {",".join(where)}'
        if limit:
            sql += f' limit {limit}'
        cursor = self.get_cursor()
        self.logger.debug(f'executing {sql}')
        cursor.execute(sql)
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
