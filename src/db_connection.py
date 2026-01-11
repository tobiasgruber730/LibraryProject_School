import mysql.connector
import json
import os
import sys


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
        """Loads database settings from JSON file. Works for both Script and EXE."""
        # Pokud běžíme jako EXE (frozen), cesta je vedle spouštěcího souboru
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            # Pokud běžíme v PyCharmu
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        config_path = os.path.join(base_dir, 'config', 'settings.json')

        try:
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data['database']
        except FileNotFoundError:
            # Tady přidáme input, aby se okno hned nezavřelo a viděl jsi chybu
            print(f"CRITICAL ERROR: Config file not found at {config_path}")
            print("Make sure 'config' folder is next to the .exe file.")
            if getattr(sys, 'frozen', False):
                input("Press Enter to exit...")
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
                database=self.config['database'],
                use_pure=True
            )
            return self.connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close(self):
        """Closes the connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()