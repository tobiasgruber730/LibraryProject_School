import mysql.connector
import json
import os


class DatabaseConnection:
    """
    Singleton class to handle database connection.
    Reads configuration from config/settings.json.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Loads database settings from JSON file."""
        # Calculate path to config file relative to this script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config', 'settings.json')

        try:
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data['database']
        except FileNotFoundError:
            print(f"Error: Config file not found at {config_path}")
            return None

    def connect(self):
        """Establishes connection to the database."""
        if self.config is None:
            return None

        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            # print("Successfully connected to the database.") # Debug line
            return self.connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close(self):
        """Closes the connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            # print("Connection closed.")


# Test code - only runs if you execute this file directly
if __name__ == "__main__":
    db = DatabaseConnection()
    conn = db.connect()
    if conn and conn.is_connected():
        print("TEST OK: Connection successful!")
        db.close()
    else:
        print("TEST FAILED: Could not connect.")