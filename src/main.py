import sys
import os
import traceback

# Ensure we can import modules from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_connection import DatabaseConnection
from book_repository import BookRepository
from loan_service import LoanService
from import_service import ImportService
from reporting_service import ReportingService


class LibraryApp:
    """
    Main Application Entry Point.
    Provides a Command Line Interface (CLI) for the user to interact with the system.
    """

    def __init__(self):
        """
        Initializes the application by instantiating all necessary services and repositories.
        """
        self.book_repo = BookRepository()
        self.loan_service = LoanService()
        self.import_service = ImportService()
        self.report_service = ReportingService()

    def print_menu(self):
        """
        Displays the main menu options to the console.
        """
        print("\n" + "=" * 30)
        print("   LIBRARY MANAGER v1.1")
        print("=" * 30)
        print("1. List All Books (with Availability)")
        print("2. Add New Book")
        print("3. Borrow a Book (Transaction)")
        print("4. Show Active Loans")
        print("5. Import Books from CSV")
        print("6. Generate Statistics Report")
        print("7. Delete a Book")
        print("8. Return a Book")
        print("0. Exit")
        print("-" * 30)

    def run(self):
        """
        Starts the main application loop.
        It handles database connection verification and user input processing.
        """
        # Initial DB Check
        db = DatabaseConnection()
        if not db.connect():
            print("CRITICAL ERROR: Cannot connect to database. Check config/settings.json.")
            input("Press Enter to exit...")
            return

        while True:
            self.print_menu()
            choice = input("Select an option: ")

            try:
                if choice == '1':
                    self.show_books()
                elif choice == '2':
                    self.add_book_ui()
                elif choice == '3':
                    self.borrow_book_ui()
                elif choice == '4':
                    self.show_loans()
                elif choice == '5':
                    self.import_csv_ui()
                elif choice == '6':
                    self.show_report()
                elif choice == '7':
                    self.delete_book_ui()
                elif choice == '8':
                    self.return_book_ui()
                elif choice == '0':
                    print("Exiting application. Goodbye!")
                    break
                else:
                    print("Invalid choice, please try again.")
            except Exception as e:
                print(f"Unexpected Application Error: {e}")

    # --- UI METHODS (User Interaction Layer) ---

    def show_books(self):
        """
        Displays all books formatted as a table.
        It also checks dynamic availability based on active loans.
        """
        print("\n--- Book List ---")
        books = self.book_repo.get_all_books()

        # Get list of currently borrowed book IDs
        borrowed_book_ids = self.loan_service.get_borrowed_book_ids()

        if not books:
            print("No books found.")

        # Print table header
        print(f"{'ID':<4} | {'Title':<30} | {'Price':<10} | {'Status'}")
        print("-" * 60)

        for b in books:
            # Determine status based on loans
            if b['book_id'] in borrowed_book_ids:
                status = "BORROWED"
            else:
                status = "AVAILABLE"

            print(f"{b['book_id']:<4} | {b['title']:<30} | {b['price']:<10.2f} | {status}")

    def add_book_ui(self):
        """
        UI for adding a new book. Displays publishers to help user selection.
        """
        print("\n--- Add New Book ---")

        print("Available Publishers:")
        publishers = self.book_repo.get_all_publishers()
        for p in publishers:
            print(f" ID {p['publisher_id']}: {p['name']}")
        print("-" * 20)

        try:
            title = input("Title: ")
            isbn = input("ISBN: ")
            price = float(input("Price: "))
            publisher_id = int(input("Publisher ID (choose from above): "))

            result = self.book_repo.add_book(title, isbn, price, publisher_id)
            if result:
                print("Book added successfully.")
            else:
                print("Failed to add book.")
        except ValueError:
            print("Error: Invalid input (price/ID must be numbers).")

    def borrow_book_ui(self):
        """
        UI for borrowing a book. Collects IDs and calls the service.
        """
        print("\n--- Borrow Book ---")
        try:
            member_id = int(input("Member ID (e.g., 1): "))
            book_id = int(input("Book ID to borrow: "))

            print("Processing transaction...")
            message = self.loan_service.borrow_book(member_id, book_id)
            print(f"Result: {message}")
        except ValueError:
            print("Error: IDs must be numbers.")

    def return_book_ui(self):
        """
        UI for returning a book.
        """
        print("\n--- Return Book ---")
        try:
            book_id = int(input("Enter Book ID to return: "))
            message = self.loan_service.return_book(book_id)
            print(message)
        except ValueError:
            print("Error: ID must be a number.")

    def show_loans(self):
        """
        UI to display currently active loans.
        """
        print("\n--- Active Loans ---")
        loans = self.loan_service.get_active_loans()
        if not loans:
            print("No active loans.")
        for l in loans:
            print(f"Loan [{l['loan_id']}] | {l['full_name']} has '{l['title']}' (since {l['loan_date']})")

    def import_csv_ui(self):
        """
        UI for triggering CSV import.
        """
        filename = input("Enter filename in /data folder (default: import_books.csv): ")
        if not filename: filename = "import_books.csv"
        print(f"Importing from {filename}...")
        print(self.import_service.import_books_from_csv(filename))

    def show_report(self):
        """
        UI for displaying statistics.
        """
        print(self.report_service.generate_top_borrowers_report())

    def delete_book_ui(self):
        """
        UI for deleting a book.
        """
        print("\n--- Delete Book ---")
        try:
            book_id = int(input("Enter Book ID to delete: "))
            confirm = input(f"Are you sure you want to delete book {book_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                if self.book_repo.delete_book(book_id):
                    print("Book deleted successfully.")
                else:
                    print("Failed to delete book (maybe ID does not exist).")
            else:
                print("Deletion cancelled.")
        except ValueError:
            print("Error: ID must be a number.")


if __name__ == "__main__":
    # Wrap main execution in a global try-except block to prevent immediate closure
    # of the console window in case of fatal errors during EXE execution.
    try:
        app = LibraryApp()
        app.run()
    except Exception:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("FATAL ERROR - PROGRAM CRASHED")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        traceback.print_exc()
        print("\n")
        input("Press ENTER to exit...")