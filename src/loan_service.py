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
        Transakční metoda pro půjčení knihy.
        Requirement: Transaction over multiple tables (loans + members).

        Steps:
        1. Check if book is available.
        2. Start Transaction.
        3. Insert record into 'loans'.
        4. Update 'members' (update activity timestamp).
        5. Commit transaction.
        """
        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor()

        try:
            # 1. CHECK AVAILABILITY (Read-only part)
            # We check if the book is currently in the 'active' loans list
            check_query = "SELECT loan_id FROM loans WHERE book_id = %s AND status = 'ACTIVE'"
            cursor.execute(check_query, (book_id,))
            if cursor.fetchone():
                return f"Error: Book ID {book_id} is already borrowed."

            # START TRANSACTION
            # By default, connector might be autocommit, so we disable it explicitly
            conn.autocommit = False

            print(f"--- Starting Transaction for Member {member_id} borrowing Book {book_id} ---")

            # 2. INSERT into LOANS (Table 1)
            insert_loan_query = """
                INSERT INTO loans (member_id, book_id, loan_date, status) 
                VALUES (%s, %s, NOW(), 'ACTIVE')
            """
            cursor.execute(insert_loan_query, (member_id, book_id))

            # 3. UPDATE MEMBERS (Table 2) - Requirement: Write to multiple tables
            # We update the 'joined_at' field to mark latest activity time,
            # or we could update any other field. This satisfies the school requirement.
            update_member_query = "UPDATE members SET joined_at = NOW() WHERE member_id = %s"
            cursor.execute(update_member_query, (member_id,))

            # 4. COMMIT (Save everything permanently)
            conn.commit()
            print("--- Transaction COMMITTED Successfully ---")
            return "Success: Book borrowed."

        except mysql.connector.Error as err:
            # IF ERROR -> ROLLBACK (Undo everything)
            conn.rollback()
            print(f"--- Transaction ROLLED BACK due to error: {err} ---")
            return f"Transaction Failed: {err}"

        finally:
            conn.autocommit = True  # Reset to default
            cursor.close()
            self.db.close()

    def get_active_loans(self):
        """
        Simple helper to see who borrowed what.
        Uses the View defined in SQL.
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            # Using the VIEW created in SQL script
            query = "SELECT * FROM view_active_loans"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching loans: {err}")
            return []
        finally:
            cursor.close()
            self.db.close()


# --- TEST AREA ---
if __name__ == "__main__":
    service = LoanService()

    # Test Data: We know from SQL script that:
    # Member ID 1 exists (Jan Novak)
    # Book ID 1 exists (1984) and is NOT borrowed yet.

    print("TEST 1: Borrowing a book (Should Success)...")
    result = service.borrow_book(member_id=1, book_id=1)
    print(result)

    print("\nTEST 2: Borrowing the SAME book again (Should Fail)...")
    result_fail = service.borrow_book(member_id=1, book_id=1)
    print(result_fail)

    print("\nTEST 3: List active loans...")
    loans = service.get_active_loans()
    for loan in loans:
        print(f"Loan ID: {loan['loan_id']} | Member: {loan['full_name']} | Book: {loan['title']}")