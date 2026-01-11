import mysql.connector
from datetime import datetime
from db_connection import DatabaseConnection


class LoanService:
    """
    Service class handling business logic for borrowing and returning books.

    It implements ACID transactions to ensure data integrity when modifying
    multiple tables ('loans' and 'members') simultaneously.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def borrow_book(self, member_id, book_id):
        """
        Executes a database transaction to borrow a book.

        Logic:
        1. Checks if the book is available.
        2. Starts a transaction.
        3. Inserts a record into the 'loans' table.
        4. Updates the 'members' table (modifies 'joined_at' as activity timestamp).
        5. Commits the transaction if all steps succeed.

        Args:
            member_id (int): ID of the member borrowing the book.
            book_id (int): ID of the book being borrowed.

        Returns:
            str: A message indicating success or failure.
        """
        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor()

        try:
            # 1. CHECK AVAILABILITY
            check_query = "SELECT loan_id FROM loans WHERE book_id = %s AND status = 'ACTIVE'"
            cursor.execute(check_query, (book_id,))
            if cursor.fetchone():
                return f"Error: Book ID {book_id} is already borrowed."

            # START TRANSACTION
            # We explicitly disable autocommit to handle the transaction manually
            conn.autocommit = False

            print(f"--- Starting Transaction for Member {member_id} borrowing Book {book_id} ---")

            # 2. INSERT into LOANS (Table 1 modification)
            insert_loan_query = """
                INSERT INTO loans (member_id, book_id, loan_date, status) 
                VALUES (%s, %s, NOW(), 'ACTIVE')
            """
            cursor.execute(insert_loan_query, (member_id, book_id))

            # 3. UPDATE MEMBERS (Table 2 modification)
            # Fulfills requirement: Update information stored in more than one table.
            update_member_query = "UPDATE members SET joined_at = NOW() WHERE member_id = %s"
            cursor.execute(update_member_query, (member_id,))

            # 4. COMMIT
            # If we reach this point without error, we save changes.
            conn.commit()
            print("--- Transaction COMMITTED Successfully ---")
            return "Success: Book borrowed."

        except mysql.connector.Error as err:
            # ROLLBACK
            # If any error occurs, we undo all changes in this transaction.
            conn.rollback()
            print(f"--- Transaction ROLLED BACK: {err} ---")
            return f"Transaction Failed: {err}"

        finally:
            if conn.is_connected():
                conn.autocommit = True
                cursor.close()
                self.db.close()

    def return_book(self, book_id):
        """
        Marks a borrowed book as returned.
        Updates the 'loans' table by setting status to 'RETURNED' and adding a return date.

        Args:
            book_id (int): The ID of the book to return.
        """
        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor()
        try:
            # Verify active loan exists
            check_query = "SELECT loan_id FROM loans WHERE book_id = %s AND status = 'ACTIVE'"
            cursor.execute(check_query, (book_id,))
            loan = cursor.fetchone()

            if not loan:
                return f"Error: Book ID {book_id} is not currently borrowed."

            # Update loan status
            update_query = """
                UPDATE loans 
                SET status = 'RETURNED', return_date = NOW() 
                WHERE loan_id = %s
            """
            cursor.execute(update_query, (loan[0],))
            conn.commit()
            return "Success: Book returned."

        except mysql.connector.Error as err:
            return f"Error returning book: {err}"
        finally:
            cursor.close()
            self.db.close()

    def get_active_loans(self):
        """
        Retrieves a list of all currently active loans.
        Uses a database VIEW 'view_active_loans' for simplified data access.

        Returns:
            list[dict]: List of active loans with member and book details.
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM view_active_loans"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching loans: {err}")
            return []
        finally:
            cursor.close()
            self.db.close()

    def get_borrowed_book_ids(self):
        """
        Helper method to retrieve a simple list of Book IDs that are currently borrowed.
        Used by the UI to determine book availability status.

        Returns:
            list[int]: List of Book IDs.
        """
        conn = self.db.connect()
        if not conn:
            return []

        cursor = conn.cursor()
        try:
            query = "SELECT book_id FROM loans WHERE status = 'ACTIVE'"
            cursor.execute(query)
            # Flattens the list of tuples [(1,), (5,)] into [1, 5]
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Error fetching borrowed IDs: {err}")
            return []
        finally:
            cursor.close()
            self.db.close()