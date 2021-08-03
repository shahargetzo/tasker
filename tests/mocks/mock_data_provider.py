from src.common.service_providers.data_provider import DataProvider


class MockDataProvider(DataProvider):
    def __init__(self, logger):
        super().__init__(logger)

    def execute_with_data(self, sql: str, values: tuple) -> int:
        self.logger.info(f'executing {sql} with values {values}')
        return -1

    def insert(self, table_name: str, keys: list, values: tuple) -> bool:
        self.logger.info(f'inserting to table {table_name}, keys {keys}, values: {values}')
        return True

    def execute(self, sql):
        self.logger.info(f'executing {sql}')

    def fetch_all(self):
        pass

    def get_cursor(self, buffered=False):
        pass

    def execute_and_fetch_all(self, sql):
        self.logger.info(f'executing {sql}')

    def update_row(self, table_name: str, to_update: dict, where: list):
        self.logger.info(f'updating table {table_name}, to update {to_update}, where: {where}')

    def get_rows(self, table_name: str, where: list = None, limit: int = 0, fields: list = None) -> list:
        self.logger.info(f'getting from table {table_name}, where {where}, limit {limit}, fields {fields}')
        return []

    def create_connection(self):
        pass

    def close_connection(self):
        pass
