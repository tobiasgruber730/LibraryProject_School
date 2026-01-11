import mysql.connector
from db_connection import DatabaseConnection


class ReportingService:
    """
    Generates reports based on aggregated data.
    Requirement: Aggregated report from at least 3 tables.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def generate_top_borrowers_report(self):
        """
        Returns a list of members with count of borrowed books and total value.
        Joins: Members + Loans + Books.
        """
        conn = self.db.connect()
        if not conn:
            return "DB Connection Failed"

        cursor = conn.cursor(dictionary=True)
        try:
            # SQL Query joining 3 tables with aggregation (COUNT, SUM)
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

            # Format the output as a string report
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


# --- TEST AREA ---
if __name__ == "__main__":
    svc = ReportingService()
    print(svc.generate_top_borrowers_report())