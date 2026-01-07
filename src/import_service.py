import csv
import mysql.connector
import os
from db_connection import DatabaseConnection


class ImportService:
    """
    Handles data import from external files (CSV).
    Requirement: Import data into min. 2 tables from CSV/XML/JSON.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def import_books_from_csv(self, filename):
        """
        Reads a CSV file and inserts data into 'publishers' and 'books' tables.
        """
        # Construct full path to the file in /data folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data', filename)

        if not os.path.exists(file_path):
            return f"Error: File {filename} not found."

        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor()
        success_count = 0
        errors = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)  # Reads CSV into dictionary using headers

                for row in reader:
                    try:
                        # Data from CSV row
                        pub_name = row['publisher_name']
                        title = row['book_title']
                        isbn = row['isbn']
                        price = float(row['price'])

                        # 1. Insert Publisher (Table 1)
                        # We use simple insert. In real app, we would check if exists.
                        cursor.execute("INSERT INTO publishers (name) VALUES (%s)", (pub_name,))

                        # Get the ID of the newly created publisher
                        new_publisher_id = cursor.lastrowid

                        # 2. Insert Book (Table 2) using the publisher ID
                        cursor.execute(
                            "INSERT INTO books (title, isbn, price, publisher_id) VALUES (%s, %s, %s, %s)",
                            (title, isbn, price, new_publisher_id)
                        )

                        conn.commit()  # Save changes for this row
                        success_count += 1
                        print(f"Imported: {title} (Publisher: {pub_name})")

                    except mysql.connector.Error as err:
                        # If one row fails (e.g. duplicate ISBN), we log it but continue with others
                        errors.append(f"Failed to import {row.get('book_title', 'Unknown')}: {err}")
                        conn.rollback()
                    except ValueError:
                        errors.append(f"Invalid data format in row: {row}")

            # Final Report
            result_msg = f"\n--- Import Finished ---\nSuccess: {success_count}\nErrors: {len(errors)}"
            if errors:
                result_msg += "\nError Details:\n" + "\n".join(errors)

            return result_msg

        except Exception as e:
            return f"Critical Error during import: {e}"

        finally:
            cursor.close()
            self.db.close()


# --- TEST AREA ---
if __name__ == "__main__":
    importer = ImportService()

    print("Starting CSV Import...")
    # Make sure 'import_books.csv' is in your 'data' folder
    print(importer.import_books_from_csv("import_books.csv"))