-- DATABASE SCHEMA FOR LIBRARY PROJECT
-- Author: [Tobiáš Gruber]
-- Date: 2026
-- Project requirement: 5 tables, 2 views, M:N relation, transaction ready

SET FOREIGN_KEY_CHECKS=0;

-- 1. Table: Authors (Simple entity)
DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NULL, -- Requirement: Date type
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP -- Requirement: DateTime type
) ENGINE=InnoDB;

-- 2. Table: Publishers (Simple entity)
DROP TABLE IF EXISTS publishers;
CREATE TABLE publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    website VARCHAR(255) NULL
) ENGINE=InnoDB;

-- 3. Table: Books (Main entity)
DROP TABLE IF EXISTS books;
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL, -- Requirement: String
    isbn VARCHAR(20) UNIQUE NOT NULL,
    price FLOAT NOT NULL, -- Requirement: Float (Real number)
    is_active TINYINT(1) DEFAULT 1, -- Requirement: Bool (1=True, 0=False)
    publisher_id INT,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
) ENGINE=InnoDB;

-- 4. Table: Members (Users who borrow books)
DROP TABLE IF EXISTS members;
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    membership_type ENUM('BASIC', 'PREMIUM', 'STUDENT') DEFAULT 'BASIC', -- Requirement: Enum
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 5. Table: Loans (Transactional table, links Members and Books M:N logic)
DROP TABLE IF EXISTS loans;
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    return_date DATETIME NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE', -- active, returned, overdue
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
) ENGINE=InnoDB;

-- 6. Table: Book_Authors (M:N Relationship table)
-- Requirement: 1x M:N relationship (One book can have multiple authors)
DROP TABLE IF EXISTS book_authors;
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Requirement: 2x Views

-- View 1: Available Books (Active books that are not currently borrowed)
CREATE OR REPLACE VIEW view_available_books AS
SELECT b.book_id, b.title, b.isbn, b.price
FROM books b
WHERE b.is_active = 1
AND b.book_id NOT IN (SELECT book_id FROM loans WHERE status = 'ACTIVE');

-- View 2: Overdue Loans (Just an example logic for reporting)
CREATE OR REPLACE VIEW view_active_loans AS
SELECT l.loan_id, m.full_name, b.title, l.loan_date
FROM loans l
JOIN members m ON l.member_id = m.member_id
JOIN books b ON l.book_id = b.book_id
WHERE l.status = 'ACTIVE';

SET FOREIGN_KEY_CHECKS=1;

-- INSERT TEST DATA (Requirement: DML commands)
INSERT INTO publishers (name) VALUES ('Penguin Books'), ('O Reilly');
INSERT INTO authors (first_name, last_name, birth_date) VALUES ('George', 'Orwell', '1903-06-25'), ('Guido', 'van Rossum', '1956-01-31');
INSERT INTO members (full_name, email, membership_type) VALUES ('Jan Novak', 'jan@test.com', 'STUDENT');
INSERT INTO books (title, isbn, price, publisher_id) VALUES ('1984', '123-456', 299.50, 1), ('Python Guide', '999-000', 500.00, 2);
INSERT INTO book_authors (book_id, author_id) VALUES (1, 1), (2, 2);