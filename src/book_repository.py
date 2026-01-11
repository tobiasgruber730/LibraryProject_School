import mysql.connector
from db_connection import DatabaseConnection


class BookRepository:
    """
    Implements the Repository Pattern for the Book entity.

    This class abstracts all direct SQL operations related to books,
    providing a clean API for the rest of the application.
    Requirement D1: Repository Pattern implementation.
    """

    def __init__(self):
        """
        Initializes the repository with a database connection instance.
        """
        self.db = DatabaseConnection()

    def get_all_books(self):
        """
        Retrieves all books from the database.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a book.
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
        Retrieves all publishers from the database.
        This is a helper method to assist users in selecting a Publisher ID when creating a book.

        Returns:
            list[dict]: A list of publishers.
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
        Inserts a new book record into the database.

        Args:
            title (str): Title of the book.
            isbn (str): International Standard Book Number.
            price (float): Price of the book.
            publisher_id (int): Foreign key referencing the publisher.

        Returns:
            int: The ID of the newly created book.
            None: If the operation fails.
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

    def delete_book(self, book_id):
        """
        Deletes a book from the database by its ID.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
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