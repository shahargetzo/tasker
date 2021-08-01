import os
from pathlib import Path

from src.common.databases_struct import process_config, job_events, jobs

db_struct_files = {process_config.table_name: process_config,
                   job_events.table_name: job_events,
                   jobs.table_name: jobs}


def validate_db_struct(statement):
    table_name = statement[len('CREATE TABLE '):statement.index('(')]
    table_name = table_name.strip()
    db_strict_module = db_struct_files.get(table_name)
    if not db_strict_module:
        raise Exception(f'no db struct for {table_name}')
    keys_in_db_struct = list(filter(lambda x: x.startswith('key_'), dir(db_strict_module)))
    keys_vals_in_db_struct = list(map(lambda x: getattr(db_strict_module, x), keys_in_db_struct))
    last_pattern_to_find = 'primary key' if 'primary key' in statement else ')'
    db_existing_keys = statement[statement.index('('): statement.rindex(last_pattern_to_find)].split(',')
    db_existing_keys = list(map(lambda x: x.split(' ')[2].strip(), db_existing_keys))
    missing_from_db_struct = list(filter(lambda x: x and x not in keys_vals_in_db_struct, db_existing_keys))
    if missing_from_db_struct:
        raise Exception(f'keys {missing_from_db_struct} are missing from db struct of {table_name}')
    extra_in_db_struct = list(filter(lambda x: x not in db_existing_keys, keys_vals_in_db_struct))
    if extra_in_db_struct:
        raise Exception(f'keys {extra_in_db_struct} are missing from sql ini of {table_name}')


def validate_tables():
    sql_ini_file_path = os.path.join(str(Path.home()), 'init.sql')
    with open(sql_ini_file_path) as f:
        ini_content = f.read()
        statements = ini_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement.startswith('CREATE TABLE'):
                validate_db_struct(statement)


if __name__ == '__main__':
    validate_tables()
