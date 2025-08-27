from db import clear_all, init_db, add_book, add_user, list_books, list_users, borrow_book, return_book
from exporttoexcel import export_top_books
init_db()

clear_all()
# Add data
u1 = add_user("Aniket", "Student")
u2 = add_user("Dr. Sharma", "Teacher")
b1 = add_book("Rich Dad Poor Dad", "Robert Kiyosaki")

print(" Before Borrow:", list_books())
print(" Users:", list_users())

print(borrow_book(u1, b1))  # should succeed
print(" After Borrow:", list_books())

print(return_book(u1, b1))  # should succeed
print(" After Return:", list_books())

export_top_books() 