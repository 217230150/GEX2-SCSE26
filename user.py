## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    category = str(category).strip().lower()

    return [
        book_id
        for book_id, book in books.items()
        if str(book["category"]).strip().lower() == category
    ]

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    search_text = str(search_text).strip().lower()

    return [
        book_id
        for book_id, book in books.items()
        if search_text in str(book["title"]).lower()
    ]
    



## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not str(borrower).strip():
        return "EMPTY_NAME"

    if not books[book_id]["available"]:
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append(
        {"book_id": book_id, "borrower": str(borrower).strip()}
    )

    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not str(borrower).strip():
        return "EMPTY_NAME"

    for loan in loans:
        if loan["book_id"] == book_id:
            loans.remove(loan)
            books[book_id]["available"] = True
            return "OK"

    return "NOT_ON_LOAN"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")
    books = data["books"]
    loans = data["loans"]

    print("LIBRARY USER SYSTEM")
    print("=" * 60)

    while True:
        print()
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            search_text = input(
                "Enter full or partial title: "
            )
            results = search_by_title(books, search_text)

            if results:
                for book_id in results:
                    print(
                        f"{book_id} | {books[book_id]['title']} | "
                        f"{books[book_id]['category']}"
                    )
            else:
                print("No books found.")

        elif choice == "2":
            category = input("Enter a category: ")
            results = books_in_category(books, category)

            if results:
                for book_id in results:
                    print(
                        f"{book_id} | {books[book_id]['title']} | "
                        f"{books[book_id]['category']}"
                    )
            else:
                print("No books found in that category.")

        elif choice == "3":
            search_text = input(
                "Enter book title, author, or ID: "
            )
            borrower = input("Enter your name: ")

            result = borrow_book(
                books,
                loans,
                search_text,
                borrower
            )

            if result == "OK":
                print("Book borrowed successfully.")
            elif result == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif result == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif result == "NOT_AVAILABLE":
                print("That book is currently on loan.")

        elif choice == "4":
            book_title = input(
                "Enter book title, author, or ID: "
            )
            borrower = input("Enter your name: ")

            result = return_book(
                books,
                loans,
                book_title,
                borrower
            )

            if result == "OK":
                print("Book returned successfully.")
            elif result == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif result == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif result == "NOT_ON_LOAN":
                print("That book is not currently on loan.")

        elif choice == "5":
            save_library(data, "library.json")
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
