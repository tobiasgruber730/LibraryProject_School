# Project Documentation: Library Manager

**Project Name:** Library Manager
**Author:** Tobiáš Gruber
**Contact:** gruber2@spsejecna.cz
**School:** SPŠE Ječná
**Date:** January 2026
**Type:** School Project (Option D1 - Repository Pattern)

---

## 1. Project Summary
The goal of this project was to create a console application in Python for managing a book collection and loans. The application demonstrates the use of a MySQL relational database, transactional data processing, and the Repository design pattern. The project meets all specified requirements, including data import, report generation, and application layer separation. The application is fully functional and ready for deployment on school PCs.

---

## 2. Requirements Specification and Use Cases
The application is designed for a librarian who needs to efficiently manage the library collection.

**Main Use Cases:**
1.  **Book Management:** The user can view the list of books, add a new book, and delete an existing book.
2.  **Loans (Transactions):** The user can process a book loan for a member. This process runs within a database transaction (writing to the loans table + updating member activity timestamp).
3.  **Data Import:** The user can bulk upload books and publishers from a CSV file.
4.  **Reporting:** The user can generate a statistical overview of the most active members and the total value of borrowed books.

---

## 3. Application Architecture
The project utilizes a layered architecture to separate business logic from data access.

### Design Patterns Used
* **Repository Pattern (D1):** The `BookRepository` class encapsulates all logic for accessing the book table. The rest of the application contains no direct SQL queries regarding books.
* **Service Layer:** The `LoanService`, `ImportService`, and `ReportingService` classes handle business logic (transactions, validation, aggregation).
* **Singleton:** The `DatabaseConnection` class ensures a single, shared connection instance to the database.

### Project Structure
* `/src`: Source codes (modules, services, repositories).
* `/data`: SQL scripts for the database and CSV files for import.
* `/config`: Configuration files.
* `/tests` / `/doc`: Documentation and test scenarios.
* `/bin`: Compiled executable files (if applicable).

---

## 4. Database Model (E-R Model)
The application uses a MySQL relational database. The database export is located in `data/database_schema.sql` and includes both DDL and DML commands.

**Tables and Attributes:**
* **authors:** `author_id` (PK), `first_name`, `last_name`, `birth_date` (Date).
* **publishers:** `publisher_id` (PK), `name` (String), `website`.
* **books:** `book_id` (PK), `title` (String), `isbn` (Unique), `price` (Float), `is_active` (Bool), `publisher_id` (FK).
* **members:** `member_id` (PK), `full_name`, `email`, `membership_type` (Enum: BASIC/PREMIUM/STUDENT), `joined_at` (Datetime).
* **loans:** `loan_id` (PK), `member_id` (FK), `book_id` (FK), `loan_date`, `status`.
* **book_authors:** M:N Junction table linking books and authors.

---

## 5. Imported Files Schema
The application supports importing books from CSV format. The import automatically populates two tables (`publishers` and `books`).

**File:** `/data/import_books.csv`
**Format:** Comma-separated text file, UTF-8 encoding.
**Required Header and Structure:**
`publisher_name,book_title,isbn,price`

**Item Description:**
* `publisher_name`: Name of the publisher (String)
* `book_title`: Title of the book (String)
* `isbn`: Unique Identifier (String)
* `price`: Price (Float)

---

## 6. Configuration
Application settings are stored in `config/settings.json`.

**Admissible Options:**
```json
{
    "database": {
        "host": "localhost",      // Database server address
        "user": "root",           // Database username
        "password": "",           // Database password
        "database": "library_db"  // Database name
    },
    "app": {
        "name": "Library Manager v1.0",
        "currency": "CZK"
    }
}