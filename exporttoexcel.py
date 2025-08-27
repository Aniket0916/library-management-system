import csv
from db import get_connection

def export_top_books(filename="top_books.csv"):
    with get_connection() as conn:
        rows= conn.execute("""
            SELECT books.bookname, COUNT(*) as borrow_count
            FROM transactions
            JOIN books ON transactions.book_id = books.id
            WHERE action = 'BORROW'
            GROUP BY books.bookname
            ORDER BY borrow_count DESC
            LIMIT 5;
        """).fetchall()

    with open(filename,"w",newline='')as f:
        writer = csv.writer(f)
        writer.writerow(["Title","Borrow Count"])
        writer.writerows(rows)

    print(f"Exported report to {filename}")

