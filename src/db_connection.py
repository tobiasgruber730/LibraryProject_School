import mysql.connector
import json
import os
import sys


class DatabaseConnection:
    """
    Singleton class responsible for managing the database connection.
    It reads configuration from 'config/settings.json' and ensures only one
    active connection configuration is loaded.
    """
    _instance = None

    def __new__(cls):
        """
        Ensures that only one instance of DatabaseConnection exists (Singleton Pattern).
        If an instance already exists, it returns the existing one.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """
        Loads database connection settings from the JSON configuration file.

        It handles path resolution for two scenarios:
        1. Running as a script (development environment).
        2. Running as a compiled EXE file (production/frozen environment).

        Returns:
            dict: Database configuration settings (host, user, password, database).
            None: If the configuration file is not found.
        """
        # Determine the base path depending on whether the app is frozen (EXE) or script
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        config_path = os.path.join(base_dir, 'config', 'settings.json')

        try:
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data['database']
        except FileNotFoundError:
            print(f"CRITICAL ERROR: Config file not found at {config_path}")
            print("Make sure 'config' folder is next to the executable.")
            if getattr(sys, 'frozen', False):
                input("Press Enter to exit...")
            return None

    def connect(self):
        """
        Establishes a connection to the MySQL database using the loaded configuration.

        Returns:
            mysql.connector.connection.MySQLConnection: The active database connection object.
            None: If the connection fails or configuration is missing.
        """
        if self.config is None:
            return None

        try:
            # 'use_pure=True' is required for compatibility with PyInstaller (EXE builds)
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                use_pure=True
            )
            return self.connection
        except mysql.connector.Error as err:
            print(f"Database Connection Error: {err}")
            return None

    def close(self):
        """
        Closes the active database connection if it exists and is open.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()