import csv
import mysql.connector
import os
import sys
from db_connection import DatabaseConnection


class ImportService:
    """
    Service responsible for importing data from external files (CSV).

    Fulfills the requirement: Import data into at least 2 tables from CSV/XML/JSON.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def import_books_from_csv(self, filename):
        """
        Reads a CSV file and inserts data into 'publishers' and 'books' tables.

        The method handles path resolution for both development (script) and
        production (EXE) environments.

        Args:
            filename (str): Name of the CSV file located in the 'data' folder.

        Returns:
            str: A report summary containing success count and error details.
        """
        # Resolve path to the data folder
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        file_path = os.path.join(base_dir, 'data', filename)

        if not os.path.exists(file_path):
            return f"Error: File {filename} not found at {file_path}. Please check /data folder."

        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor()
        success_count = 0
        errors = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    try:
                        # Extract data from CSV row
                        pub_name = row['publisher_name']
                        title = row['book_title']
                        isbn = row['isbn']
                        price = float(row['price'])

                        # 1. Insert into Publishers table
                        cursor.execute("INSERT INTO publishers (name) VALUES (%s)", (pub_name,))
                        new_publisher_id = cursor.lastrowid

                        # 2. Insert into Books table (linked to the new publisher)
                        cursor.execute(
                            "INSERT INTO books (title, isbn, price, publisher_id) VALUES (%s, %s, %s, %s)",
                            (title, isbn, price, new_publisher_id)
                        )

                        conn.commit()
                        success_count += 1
                        print(f"Imported: {title} (Publisher: {pub_name})")

                    except mysql.connector.Error as err:
                        errors.append(f"Failed to import {row.get('book_title', 'Unknown')}: {err}")
                        conn.rollback()
                    except ValueError:
                        errors.append(f"Invalid data format in row: {row}")

            # Generate final report
            result_msg = f"\n--- Import Finished ---\nSuccess: {success_count}\nErrors: {len(errors)}"
            if errors:
                result_msg += "\nError Details:\n" + "\n".join(errors)

            return result_msg

        except Exception as e:
            return f"Critical Error during import: {e}"

        finally:
            if 'cursor' in locals(): cursor.close()
            self.db.close()