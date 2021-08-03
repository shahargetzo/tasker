import os

from src.common.databases_struct import db_validator
from tests import ut_constants


def test_db_struct_matches_sql_file():
    db_validator.validate_tables(os.path.join(ut_constants.tasker_root_dir, 'db', 'init.sql'))
