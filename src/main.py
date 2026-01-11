import sys
import os

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
    Provides CLI (Command Line Interface) for the user.
    """

    def __init__(self):
        self.book_repo = BookRepository()
        self.loan_service = LoanService()
        self.import_service = ImportService()
        self.report_service = ReportingService()

    def print_menu(self):
        print("\n" + "="*30)
        print("   LIBRARY MANAGER v1.0")
        print("="*30)
        print("1. List All Books")
        print("2. Add New Book")
        print("3. Borrow a Book (Transaction)")
        print("4. Show Active Loans")
        print("5. Import Books from CSV")
        print("6. Generate Statistics Report")
        print("7. Delete a Book")  # <--- NOVÉ
        print("0. Exit")
        print("-" * 30)

    def run(self):
        # ... (zbytek zůstává stejný) ...
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
                elif choice == '7':            # <--- NOVÉ
                    self.delete_book_ui()      # <--- NOVÉ
                elif choice == '0':
                    print("Exiting application. Goodbye!")
                    break
                else:
                    print("Invalid choice, please try again.")
            except Exception as e:
                print(f"Unexpected Application Error: {e}")

    # ... (ostatní metody zůstávají) ...

    # Přidej tuto metodu dolů mezi ostatní UI metody:
    def delete_book_ui(self):
        print("\n--- Delete Book ---")
        try:
            book_id = int(input("Enter Book ID to delete: "))
            # Check confirmation
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

    # --- UI METHODS ---

    def show_books(self):
        print("\n--- Book List ---")
        books = self.book_repo.get_all_books()
        if not books:
            print("No books found.")
        for b in books:
            status = "Active" if b['is_active'] else "Inactive"
            print(f"[{b['book_id']}] {b['title']} (ISBN: {b['isbn']}) - {b['price']} CZK [{status}]")

    def add_book_ui(self):
        print("\n--- Add New Book ---")
        try:
            title = input("Title: ")
            isbn = input("ISBN: ")
            price = float(input("Price: "))
            # We hardcode publisher ID 1 for simplicity in this UI demo
            # In a full app, we would list publishers first
            publisher_id = input("Publisher ID (default 1): ")
            if not publisher_id: publisher_id = 1

            result = self.book_repo.add_book(title, isbn, price, publisher_id)
            if result:
                print("Book added successfully.")
            else:
                print("Failed to add book.")
        except ValueError:
            print("Error: Invalid input format (e.g. price must be a number).")

    def borrow_book_ui(self):
        print("\n--- Borrow Book ---")
        try:
            member_id = int(input("Member ID (e.g., 1): "))
            book_id = int(input("Book ID to borrow: "))

            print("Processing transaction...")
            message = self.loan_service.borrow_book(member_id, book_id)
            print(f"Result: {message}")
        except ValueError:
            print("Error: IDs must be numbers.")

    def show_loans(self):
        print("\n--- Active Loans ---")
        loans = self.loan_service.get_active_loans()
        if not loans:
            print("No active loans.")
        for l in loans:
            print(f"Loan [{l['loan_id']}] | {l['full_name']} borrowed '{l['title']}' on {l['loan_date']}")

    def import_csv_ui(self):
        filename = input("Enter filename in /data folder (default: import_books.csv): ")
        if not filename: filename = "import_books.csv"

        print(f"Importing from {filename}...")
        result = self.import_service.import_books_from_csv(filename)
        print(result)

    def show_report(self):
        print(self.report_service.generate_top_borrowers_report())


if __name__ == "__main__":
    app = LibraryApp()
    app.run()