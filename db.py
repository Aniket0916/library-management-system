import sqlite3

def get_connection():
    return sqlite3.connect("library.db")

def init_db():
    with get_connection() as conn, open("schema.sql","r") as f:
        conn.executescript(f.read())
    print("database initialized")

def add_book(bookname,author):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO books (bookname,author) VALUES (?,?);",(bookname,author)
        )
        conn.commit()
        return cur.lastrowid
    
def list_books(available_only = False):
    with get_connection() as conn:
        query= """
        SELECT b.id, b.bookname, b.author, b.is_available,
               CASE
                   WHEN last_tx.action = 'BORROW' THEN u.name
                   ELSE NULL
               END AS borrowed_by
        FROM books b
        LEFT JOIN (
            SELECT t1.book_id, t1.user_id, t1.action
            FROM transactions t1
            WHERE t1.rowid = (
                SELECT MAX(t2.rowid)
                FROM transactions t2
                WHERE t2.book_id = t1.book_id
            )
        ) last_tx ON b.id = last_tx.book_id
        LEFT JOIN users u ON last_tx.user_id = u.id
        """
        if available_only:
            query += " WHERE b.is_available = 1"
        rows = conn.execute(query).fetchall()
        print("DEbug rows:",rows)
        return rows
    
def add_user(name,user_type):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO users (name,user_type) VALUES (?,?);",(name,user_type)
        )
        conn.commit()
        return cur.lastrowid
    
def list_users():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users;").fetchall()
    
def borrow_book(user_id, book_id):
    with get_connection() as conn:
        user = conn.execute("SELECT id FROM users WHERE id=?;",(user_id,)).fetchone()
        if not user:
            return "User not found"
        book = conn.execute("SELECT is_available FROM books WHERE id =?;",(book_id,)).fetchone()
        if not book or book[0] == 0:
            return "Book not available"
        conn.execute("UPDATE books SET is_available=0 WHERE id = ?;",(book_id,))
        conn.execute("INSERT INTO transactions(user_id,book_id,action) VALUES (?,?,'BORROW');",(user_id,book_id))
        conn.commit()
        return "Book Borrowed"

def return_book(user_id, book_id):
    with get_connection() as conn:
        book = conn.execute("SELECT is_available FROM books WHERE id=?;",(book_id,)).fetchone()
        if not book:
            return "Book not found"
        
        if book[0] == 1:
            return "Book is already in library"
        
        conn.execute("UPDATE books SET is_available = 1 WHERE id = ?",(book_id,))
        conn.execute("INSERT INTO transactions (user_id ,book_id, action) VALUES (?,?,'RETURN');",(user_id,book_id))
        conn.commit()
        return "Book returned"
    
def clear_all():
    with get_connection() as conn:
        conn.execute("DELETE FROM books;")
        conn.execute("DELETE FROM users;")
        conn.execute("DELETE FROM transactions;")
        conn.commit()