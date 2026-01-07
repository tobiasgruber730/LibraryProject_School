import mysql.connector
from db_connection import DatabaseConnection


class BookRepository:
    """
    Implements the Repository Pattern for Book entity.
    Handles all SQL operations related to books.
    Requirement D1: Repository Pattern.
    """

    def __init__(self):
        # We get the singleton instance of database connection
        self.db = DatabaseConnection()

    def get_all_books(self):
        """
        Fetches all books from the database.
        Returns a list of dictionaries (one dict per book).
        """
        conn = self.db.connect()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            # Simple SELECT query
            query = "SELECT * FROM books"
            cursor.execute(query)
            books = cursor.fetchall()
            return books
        except mysql.connector.Error as err:
            print(f"Error fetching books: {err}")
            return []
        finally:
            cursor.close()
            # We do NOT close the connection here if we want to reuse it,
            # but for simple scripts, it's safer to close or rely on context managers.
            self.db.close()

    def add_book(self, title, isbn, price, publisher_id):
        """
        Inserts a new book into the database.
        Returns the ID of the new book or None if failed.
        """
        conn = self.db.connect()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            query = "INSERT INTO books (title, isbn, price, publisher_id) VALUES (%s, %s, %s, %s)"
            values = (title, isbn, price, publisher_id)
            cursor.execute(query, values)
            conn.commit()  # Important: Save changes to DB

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
            book = cursor.fetchone()
            return book
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


# --- TEST AREA (will be removed later or moved to tests) ---
if __name__ == "__main__":
    repo = BookRepository()

    print("--- TESTING REPOSITORY ---")

    # 1. Add a new book
    repo.add_book("Harry Potter", "999-888-777", 450.00, 1)

    # 2. List all books
    all_books = repo.get_all_books()
    print(f"Total books in DB: {len(all_books)}")
    for b in all_books:
        print(f" - {b['title']} ({b['isbn']})")