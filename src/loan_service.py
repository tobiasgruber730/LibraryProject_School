import mysql.connector
from datetime import datetime
from db_connection import DatabaseConnection


class LoanService:
    """
    Handles business logic for borrowing and returning books.
    Implements TRANSACTION logic over multiple tables.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def borrow_book(self, member_id, book_id):
        """
        Transaction to borrow a book.
        Inserts into loans and updates members table.
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
            conn.autocommit = False

            print(f"--- Starting Transaction for Member {member_id} borrowing Book {book_id} ---")

            # 2. INSERT into LOANS
            insert_loan_query = """
                INSERT INTO loans (member_id, book_id, loan_date, status) 
                VALUES (%s, %s, NOW(), 'ACTIVE')
            """
            cursor.execute(insert_loan_query, (member_id, book_id))

            # 3. UPDATE MEMBERS (Activity timestamp)
            update_member_query = "UPDATE members SET joined_at = NOW() WHERE member_id = %s"
            cursor.execute(update_member_query, (member_id,))

            # 4. COMMIT
            conn.commit()
            print("--- Transaction COMMITTED Successfully ---")
            return "Success: Book borrowed."

        except mysql.connector.Error as err:
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
        Marks a book as returned.
        Updates 'loans' table: sets status to 'RETURNED' and end_date to NOW.
        """
        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor()
        try:
            # Check if there is an active loan for this book
            check_query = "SELECT loan_id FROM loans WHERE book_id = %s AND status = 'ACTIVE'"
            cursor.execute(check_query, (book_id,))
            loan = cursor.fetchone()

            if not loan:
                return f"Error: Book ID {book_id} is not currently borrowed."

            # Update the loan record
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
        Returns list of active loans using the SQL View (for display purposes).
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
        Helper method to get a simple list of Book IDs that are currently borrowed.
        Fixes the issue where View didn't include IDs.
        """
        conn = self.db.connect()
        if not conn:
            return []

        cursor = conn.cursor()  # Regular cursor, not dictionary
        try:
            query = "SELECT book_id FROM loans WHERE status = 'ACTIVE'"
            cursor.execute(query)
            # Convert list of tuples [(1,), (5,)] to simple list [1, 5]
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Error fetching borrowed IDs: {err}")
            return []
        finally:
            cursor.close()
            self.db.close()