from typing import Union, Dict, Optional

class ClientBase:
    def __init__(self) -> None:
        """
        Initialize an empty database as a dictionary.
        """
        self.db: Dict[str, Dict] = {}

    def create_table(self, table_name: str) -> None:
        """
        Create a new table in the database if it doesn't already exist.

        :param table_name: The name of the table to create.
        """
        if table_name not in self.db:
            self.db[table_name] = {}

    def input(self, table_name: str, key: str, value: Union[str, int, float, Dict]) -> None:
        """
        Insert or update a value in the specified table and hierarchical key.
        If the table or upper level doesn't exist, it will be created.

        :param table_name: The name of the table where the data should be inserted.
        :param key: The hierarchical key (e.g., 'money.user').
        :param value: The value to insert or update. Can be a string, integer, float, or nested dictionary.
        """
        levels = key.split('.')
        top_level = levels[0]
        bottom_level = levels[1]

        if table_name not in self.db:
            self.create_table(table_name)

        if top_level not in self.db[table_name]:
            self.db[table_name][top_level] = {}

        self.db[table_name][top_level][bottom_level] = value

    def update(self, table_name: str, key: str, value: Union[str, int, float, Dict]) -> bool:
        """
        Update an existing value in the specified table and hierarchical key.

        :param table_name: The name of the table where the data should be updated.
        :param key: The hierarchical key (e.g., 'money.user').
        :param value: The new value to set. Can be a string, integer, float, or nested dictionary.
        :return: True if update was successful, False if the key was not found.
        """
        levels = key.split('.')
        top_level = levels[0]
        bottom_level = levels[1]

        if table_name in self.db and top_level in self.db[table_name] and bottom_level in self.db[table_name][top_level]:
            self.db[table_name][top_level][bottom_level] = value
            return True
        return False

    def delete_table(self, table_name: str) -> bool:
        """
        Delete the specified table from the database.

        :param table_name: The name of the table to delete.
        :return: True if the table was deleted, False if the table does not exist.
        """
        if table_name in self.db:
            del self.db[table_name]
            return True
        return False

    def clear_table(self, table_name: str) -> bool:
        """
        Clear all data within the specified table without deleting the table.

        :param table_name: The name of the table to clear.
        :return: True if the table was cleared, False if the table does not exist.
        """
        if table_name in self.db:
            self.db[table_name] = {}
            return True
        return False

    def show(self) -> Dict[str, Dict]:
        """
        Return the entire database content.

        :return: The dictionary representing the database.
        """
        return self.db

    def get_data(self, table_name: str, key: str) -> Optional[Union[str, int, float, Dict]]:
        """
        Retrieve data by table and key.

        :param table_name: The name of the table.
        :param key: The hierarchical key (e.g., 'money.user').
        :return: The value associated with the key, or None if not found.
        """
        levels = key.split('.')
        top_level = levels[0]
        bottom_level = levels[1]

        if table_name in self.db and top_level in self.db[table_name] and bottom_level in self.db[table_name][top_level]:
            return self.db[table_name][top_level][bottom_level]
        return None
