import unittest

class ClientBase:
    db = {}

    @classmethod
    def input(cls, table_name: str, key: str, value: int):
        """Insert or update the value in the database."""
        levels = key.split('.')
        top_level = levels[0]
        bottom_level = levels[1]

        # Create table if it doesn't exist
        if table_name not in cls.db:
            cls.db[table_name] = {}

        # Create the top-level structure if it doesn't exist
        if top_level not in cls.db[table_name]:
            cls.db[table_name][top_level] = {}

        # Insert or update the bottom-level value
        cls.db[table_name][top_level][bottom_level] = value

class TestClientBase(unittest.TestCase):
    def setUp(self):
        """Set up a fresh state before each test."""
        # Clear the database before each test
        ClientBase.db = {}

    def test_input_data(self):
        """Test inputting data into the database."""
        ClientBase.input(table_name="user", key="money.count", value=50)
        
        # Check if the data was inserted correctly
        self.assertEqual(ClientBase.db["user"]["money"]["count"], 50)

    def test_input_data_with_existing_table(self):
        """Test input when the table already exists."""
        ClientBase.input(table_name="user", key="money.count", value=50)
        ClientBase.input(table_name="user", key="money.count", value=100)

        # Check if the value is updated correctly
        self.assertEqual(ClientBase.db["user"]["money"]["count"], 100)

    def test_input_non_existing_key(self):
        """Test input with a non-existing key structure."""
        ClientBase.input(table_name="user", key="money.balance", value=200)

        # Check if the value was correctly inserted at the new key
        self.assertEqual(ClientBase.db["user"]["money"]["balance"], 200)

    def test_input_to_non_existent_table(self):
        """Test inputting to a non-existent table."""
        ClientBase.input(table_name="settings", key="theme.color", value="dark")

        # Check if the table was created with the new key
        self.assertEqual(ClientBase.db["settings"]["theme"]["color"], "dark")

if __name__ == "__main__":
    unittest.main()
