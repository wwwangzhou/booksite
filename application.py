# def main():
#     # List all books.
#     books = db.execute("SELECT * FROM books").fetchall()
#     for book in books:
#         print(f"Title : {book.title} written by {book.author} in {book.year}.")
#     print()
#
#     # List all books published @1998: just an example
#     books_found = db.execute("select * from books where year=1998;").fetchall()
#     for book in books_found:
#         print(f"Book published at 1998 : {book.title} written by {book.author} in {book.year}.")
#
#     # Prompt user to choose a year.
#     year = int(input("\nYear published: "))
#     book = db.execute("SELECT * FROM books WHERE year = :year",
#                         {"year": year}).fetchone()
#
#     # Make sure book is valid.
#     if book is None:
#         print("Error: No such book.")
#     else:
#         # List books found @ variable year.
#         books_found_at_year = db.execute("SELECT * FROM books WHERE year = :year",
#                                 {"year": year}).fetchall()
#         for book in books_found_at_year:
#             print(f"Book published at {year} : {book.title} written by {book.author} in {book.year}.")
#         if len(books) == 0:
#             print("No books found.")

from booksite import app

if __name__ == "__main__":
    # main()
    app.run(debug=True) #  python3 application.py REPLACEs flask run
# @app.route("/<string:name>")
# def hello(name):
#     name = name.capitalize()
#     return f"<h1>Hello, {name}</h1>"
