import mysql.connector
from db_connection import DatabaseConnection


class BookRepository:
    """
    Implements the Repository Pattern for Book entity.
    Handles all SQL operations related to books.
    Requirement D1: Repository Pattern.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def get_all_books(self):
        """
        Fetches all books from the database.
        Returns a list of dictionaries.
        """
        conn = self.db.connect()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM books"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching books: {err}")
            return []
        finally:
            cursor.close()
            self.db.close()

    def get_all_publishers(self):
        """
        Fetches all publishers to help user choose ID during book creation.
        """
        conn = self.db.connect()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM publishers")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching publishers: {err}")
            return []
        finally:
            cursor.close()
            self.db.close()

    def add_book(self, title, isbn, price, publisher_id):
        """
        Inserts a new book into the database.
        """
        conn = self.db.connect()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            query = "INSERT INTO books (title, isbn, price, publisher_id) VALUES (%s, %s, %s, %s)"
            values = (title, isbn, price, publisher_id)
            cursor.execute(query, values)
            conn.commit()

            new_id = cursor.lastrowid
            print(f"Success: Book '{title}' added with ID {new_id}.")
            return new_id
        except mysql.connector.Error as err:
            print(f"Error adding book: {err}")
            return None
        finally:
            cursor.close()
            self.db.close()

    def find_book_by_isbn(self, isbn):
        """
        Finds a book by its ISBN.
        """
        conn = self.db.connect()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM books WHERE isbn = %s"
            cursor.execute(query, (isbn,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error finding book: {err}")
            return None
        finally:
            cursor.close()
            self.db.close()

    def delete_book(self, book_id):
        """
        Deletes a book by ID.
        """
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        try:
            query = "DELETE FROM books WHERE book_id = %s"
            cursor.execute(query, (book_id,))
            conn.commit()
            print(f"Success: Book ID {book_id} deleted.")
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting book: {err}")
            return False
        finally:
            cursor.close()
            self.db.close()