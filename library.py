"""
Library Management System (OOP: classes, inheritance, polymorphism)
- Book (base) -> TextBook, Novel, Magazine   (different loan periods & late fees)
- User (base) -> Student, Faculty            (different borrowing limits)
- Library manages the catalogue, members, issuing and returning.
"""
from abc import ABC, abstractmethod
from datetime import date, timedelta


# ---------------------------- Books ----------------------------
class Book(ABC):
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    @abstractmethod
    def loan_days(self):
        """Number of days the book can be borrowed."""

    @abstractmethod
    def fine_per_day(self):
        """Late fine charged per day (Rs)."""

    def category(self):
        return self.__class__.__name__

    def __str__(self):
        status = "Available" if self.is_available else "Issued"
        return f"[{self.book_id}] {self.title} by {self.author} ({self.category()}) - {status}"


class TextBook(Book):
    def loan_days(self):
        return 30

    def fine_per_day(self):
        return 2


class Novel(Book):
    def loan_days(self):
        return 14

    def fine_per_day(self):
        return 5


class Magazine(Book):
    def loan_days(self):
        return 7

    def fine_per_day(self):
        return 10


# ---------------------------- Users ----------------------------
class User(ABC):
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed = {}  # book_id -> (Book, due_date)

    @abstractmethod
    def max_books(self):
        """Maximum number of books the user may hold."""

    @abstractmethod
    def loan_multiplier(self):
        """Extra loan time factor for this type of user."""

    def can_borrow(self):
        return len(self.borrowed) < self.max_books()

    def role(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.role()} {self.name} (ID {self.user_id}) - {len(self.borrowed)}/{self.max_books()} books"


class Student(User):
    def max_books(self):
        return 3

    def loan_multiplier(self):
        return 1.0


class Faculty(User):
    def max_books(self):
        return 8

    def loan_multiplier(self):
        return 2.0


# ---------------------------- Library ----------------------------
class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}
        self.users = {}

    def add_book(self, book):
        self.books[book.book_id] = book

    def add_user(self, user):
        self.users[user.user_id] = user

    def issue_book(self, user_id, book_id, issue_date=None):
        issue_date = issue_date or date.today()
        user, book = self.users.get(user_id), self.books.get(book_id)
        if user is None or book is None:
            return "Invalid user or book ID."
        if not book.is_available:
            return f"'{book.title}' is already issued."
        if not user.can_borrow():
            return f"{user.name} has reached the limit of {user.max_books()} books."
        days = int(book.loan_days() * user.loan_multiplier())
        due = issue_date + timedelta(days=days)
        user.borrowed[book_id] = (book, due)
        book.is_available = False
        return f"Issued '{book.title}' to {user.name}. Due on {due}."

    def return_book(self, user_id, book_id, return_date=None):
        return_date = return_date or date.today()
        user = self.users.get(user_id)
        if user is None or book_id not in user.borrowed:
            return "This user has not borrowed that book."
        book, due = user.borrowed.pop(book_id)
        book.is_available = True
        late = max((return_date - due).days, 0)
        fine = late * book.fine_per_day()  # polymorphic call
        msg = f"{user.name} returned '{book.title}'."
        return msg + (f" Late by {late} day(s). Fine: Rs {fine}." if late else " No fine.")

    def show_books(self):
        for b in self.books.values():
            print(b)

    def show_users(self):
        for u in self.users.values():
            print(u)


# ---------------------------- Demo / Menu ----------------------------
def demo():
    lib = Library("Central Library")
    lib.add_book(TextBook(101, "Python Programming", "Mark Lutz"))
    lib.add_book(Novel(102, "The Guide", "R. K. Narayan"))
    lib.add_book(Magazine(103, "National Geographic", "Various"))
    lib.add_book(TextBook(104, "Data Structures", "Seymour Lipschutz"))
    lib.add_user(Student(1, "Asha"))
    lib.add_user(Faculty(2, "Dr. Ravi"))

    print("=== Catalogue ===")
    lib.show_books()
    print("\n=== Issuing ===")
    print(lib.issue_book(1, 101, date(2026, 10, 1)))
    print(lib.issue_book(1, 102, date(2026, 10, 1)))
    print(lib.issue_book(2, 101))           # already issued
    print(lib.issue_book(2, 103, date(2026, 10, 1)))
    print("\n=== Returning (polymorphic fines) ===")
    print(lib.return_book(1, 102, date(2026, 10, 20)))  # Novel: 5 days late * Rs5
    print(lib.return_book(2, 103, date(2026, 10, 12)))  # Faculty gets 14 days: on time, no fine
    print(lib.return_book(1, 101, date(2026, 11, 10)))  # TextBook: 9 days late * Rs2
    print("\n=== Members ===")
    lib.show_users()


def menu():
    lib = Library("Central Library")
    lib.add_book(TextBook(101, "Python Programming", "Mark Lutz"))
    lib.add_book(Novel(102, "The Guide", "R. K. Narayan"))
    lib.add_book(Magazine(103, "National Geographic", "Various"))
    lib.add_user(Student(1, "Asha"))
    lib.add_user(Faculty(2, "Dr. Ravi"))
    while True:
        print("\n1.Show books 2.Show users 3.Issue 4.Return 5.Exit")
        ch = input("Choice: ").strip()
        if ch == "1":
            lib.show_books()
        elif ch == "2":
            lib.show_users()
        elif ch == "3":
            print(lib.issue_book(int(input("User ID: ")), int(input("Book ID: "))))
        elif ch == "4":
            print(lib.return_book(int(input("User ID: ")), int(input("Book ID: "))))
        elif ch == "5":
            break


if __name__ == "__main__":
    import sys
    menu() if "--menu" in sys.argv else demo()
