import mysql.connector
from db_connection import DatabaseConnection


class ReportingService:
    """
    Service responsible for generating statistical reports.

    Fulfills the requirement: Aggregated report from at least 3 tables.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def generate_top_borrowers_report(self):
        """
        Generates a report of members, their total loans, and total value of borrowed books.

        SQL Logic:
        - JOINS 3 tables: members, loans, books.
        - Uses Aggregation functions: COUNT() and SUM().
        - Groups results by member.

        Returns:
            str: Formatted string table suitable for console output.
        """
        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    m.full_name, 
                    m.email,
                    COUNT(l.loan_id) as total_loans, 
                    SUM(b.price) as total_value_borrowed
                FROM members m
                JOIN loans l ON m.member_id = l.member_id
                JOIN books b ON l.book_id = b.book_id
                GROUP BY m.member_id
                ORDER BY total_value_borrowed DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            # Formatting the report header
            report = "\n=== LIBRARY BORROWING REPORT ===\n"
            report += f"{'Member Name':<25} | {'Loans':<5} | {'Total Value':<10}\n"
            report += "-" * 50 + "\n"

            for row in results:
                # Handle None values if sum is null
                val = row['total_value_borrowed'] if row['total_value_borrowed'] else 0.0
                report += f"{row['full_name']:<25} | {row['total_loans']:<5} | {val:<10.2f}\n"

            report += "================================\n"
            return report

        except mysql.connector.Error as err:
            return f"Error generating report: {err}"
        finally:
            cursor.close()
            self.db.close()