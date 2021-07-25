import mysql.connector
from mysql.connector import DatabaseError

from common.service_providers.data_provider import DataProvider, config
from common.databases_struct import jobs, job_events, process_config


class DBBuilder:
    def __init__(self, logger):
        self.logger = logger
        self.data_provider = DataProvider(logger)
        self.data_provider.create_connection()

    def finish(self):
        self.data_provider.close_connection()

    def create_db_if_not_exist(self):
        db_config = config.copy()
        del db_config['database']
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(f'create database tasker')
        except DatabaseError:
            pass
        except Exception as e:
            self.logger.error(f'failed to create database: {str(e)}')
        finally:
            cursor.close()
            connection.close()

    def remove_deprecated_indexes(self, all_current_indexes: list, db_struct: list, table_name: str):
        all_needed_indexes = []
        for x in db_struct:
            if x.get('name', '').lower() == 'index':
                all_needed_indexes.append(x['type'].replace('(', '').replace(')', '').replace(',', '_'))
        self.logger.debug(
            f'table: {table_name} need indexes: {all_needed_indexes}. current indexes: {all_current_indexes}',
            table_name, all_needed_indexes, all_current_indexes)
        indexes_diff = set(all_current_indexes) - set(all_needed_indexes)
        indexes_diff.remove('PRIMARY')
        if len(indexes_diff) > 0:
            self.logger.info(f'indexes to be removed {indexes_diff}')
            for index_to_remove in list(indexes_diff):
                self.remove_index(index_to_remove, table_name)
        return table_name

    def remove_index(self, index_to_remove: str, table_name: str):
        alter_sql = f'ALTER TABLE {table_name} DROP INDEX {index_to_remove}'
        self.logger.info(f'remove index from table {table_name}. sql: {alter_sql}')
        self.data_provider.execute(alter_sql)

    def create_table_columns_and_indexes(self, db_struct: list, table_name: str):
        self.logger.info(f'verifying table {table_name} columns')
        all_current_columns = self.get_all_current_columns(table_name)
        self.update_table_fields(all_current_columns, db_struct, table_name)
        all_current_indexes = self.get_all_current_indexes(table_name)
        self.remove_deprecated_indexes(all_current_indexes, db_struct, table_name)
        self.create_new_indexes(all_current_indexes, db_struct, table_name)

    def create_table_if_not_exist(self, db_struct: list, table_name: str):
        sql_statement = f'CREATE TABLE if not exists {table_name} ('
        sql_statement += get_fields_to_create(db_struct)
        sql_statement = sql_statement[:-1] + ')'
        self.logger.debug(f'run sql query : {sql_statement}')
        self.data_provider.execute(sql_statement)

    def get_all_current_columns(self, table_name):
        all_current_columns = self.data_provider.execute_and_fetch_all(f'SHOW COLUMNS FROM {table_name}')
        return list(map(lambda x: x[0], all_current_columns))

    def get_all_current_indexes(self, table_name):
        all_current_indexes = self.data_provider.execute_and_fetch_all(f'SHOW index FROM {table_name}')
        return list(map(lambda x: x[2], all_current_indexes))

    def update_table_fields(self, all_current_columns, db_struct, table_name):
        make_update = False
        alter_sql = f'ALTER TABLE {table_name}'
        for x in db_struct:
            if 'name' in x and x['name'].lower() != 'index':
                if x['name'] in all_current_columns:
                    continue
                make_update = True
                alter_sql += f' ADD COLUMN {x["name"]} {x["type"]}'
                if 'rule' in x:
                    alter_sql += f' {x["rule"]} '
                alter_sql += ','
        if make_update:
            alter_sql = alter_sql[:-1]
            self.data_provider.execute(alter_sql)

    def create_new_indexes(self, all_current_indexes, db_struct, table_name):
        for x in db_struct:
            if x.get('name', '').lower() == 'index':
                index_name = x['type'].replace('(', '').replace(')', '').replace(',', '_')
                if index_name in all_current_indexes:
                    continue
                alter_sql = f'CREATE index {index_name} ON {table_name} {x["type"].replace("_", ",")}'
                self.data_provider.execute(alter_sql)

    def create_tables_if_nor_exist(self):
        for table_class in [jobs, job_events, process_config]:
            self.create_table_if_not_exist(table_class.db_struct, table_class.table_name)
            self.create_table_columns_and_indexes(table_class.db_struct, table_class.table_name)


def get_fields_to_create(db_struct):
    sql_statement = ''
    for x in db_struct:
        name = x.get('name', '')
        field_type = x.get('type', '')
        sql_statement += f'{name} '
        if name.lower() == 'index':
            sql_statement += field_type.replace('_', ',')
        else:
            sql_statement += field_type
        rule_ = x.get('rule')
        if rule_ in x:
            sql_statement += f' {rule_} '
        sql_statement += ','
    return sql_statement
