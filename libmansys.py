class Book:
    def __init__(self,bookname,author):
        self.bookname = bookname
        self.author = author
        self.is_available = True
    def __str__(self):
        status = "Available" if self.is_available else "Issued"
        return f"{self.bookname} by {self.author} [{status}]"
        
class User:
    def __init__(self,name):
        self.name = name
        self.borrowed_books= []

    def borrow_book(self,book):
        if book.is_available:
            book.is_available = False
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed {book.bookname}")
        else:
            print(f"{book.bookname} is not available ")

    def return_book(self,book):
        if book in self.borrowed_books:
            book.is_available = True
            self.borrowed_books.remove(book)
            print(f"{self.name} returned {book.bookname}")
        else:
            print(f"{self.name} did not borrow {book.bookname}")

class Student(User):
    def __init__(self,name,student_id):
        super().__init__(name)
        self.student_id = student_id

class Teacher(User):
    def __init__(self,name,employee_id):
        super().__init__(name)
        self.employee_id = employee_id

class Library:
    def __init__(self,name):
        self.name = name
        self.books=[]

    def add_book(self,book):
        self.books.append(book)
        print(f"{book.bookname} added to {self.name} library")

    def show_available_books(self):
        print(f"\n Available Books in {self.name} Library:")
        available = False
        for book in self.books:
            if book.is_available:
                print(book)
                available = True
        if not available:
            print("No books available right now!")

# -------------------------------
# Main Program (Test LMS)
# -------------------------------
if __name__ == "__main__":
    # Create Library
    my_library = Library("Central")

    # Add Books
    b1 = Book("The Alchemist", "Paulo Coelho")
    b2 = Book("Python Crash Course", "Eric Matthes")
    b3 = Book("Rich Dad Poor Dad", "Robert Kiyosaki")
    b4 = Book("Clean Code", "Robert C. Martin")

    my_library.add_book(b1)
    my_library.add_book(b2)
    my_library.add_book(b3)
    my_library.add_book(b4)

    # Create Users
    student1 = Student("Aniket", "S101")
    student2 = Student("Ravi", "S102")
    teacher1 = Teacher("Dr. Sharma", "T202")

    # Show available books initially
    my_library.show_available_books()

    # Borrow Books
    student1.borrow_book(b1)    # success
    teacher1.borrow_book(b2)    # success
    student2.borrow_book(b2)    # ❌ already issued

    # Show available after borrowing
    my_library.show_available_books()

    # Return Books
    student1.return_book(b1)    # success
    student1.return_book(b3)    # ❌ student1 never borrowed this book
    teacher1.return_book(b2)    # success

    # Show available after returns
    my_library.show_available_books()

    # Borrow again after return
    student2.borrow_book(b2)    # now Ravi can borrow it
    my_library.show_available_books()
