import os,datetime, csv

from flask import Flask,render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# bridge the connection between Python and Database
engine = create_engine(os.getenv("DATABASE_URL"))

# allow each user have her/his own workspace
db = scoped_session(sessionmaker(bind=engine))

# create an instance of Flask class
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def main():
    # List all books.
    books = db.execute("SELECT * FROM books").fetchall()
    for book in books:
        print(f"Title : {book.title} written by {book.author} in {book.year}.")
    print()

    # List all books published @1998: just an example
    books_found = db.execute("select * from books where year=1998;").fetchall()
    for book in books_found:
        print(f"Book published at 1998 : {book.title} written by {book.author} in {book.year}.")

    # Prompt user to choose a year.
    year = int(input("\nYear published: "))
    book = db.execute("SELECT * FROM books WHERE year = :year",
                        {"year": year}).fetchone()

    # Make sure book is valid.
    if book is None:
        print("Error: No such book.")
    else:
        # List books found @ variable year.
        books_found_at_year = db.execute("SELECT * FROM books WHERE year = :year",
                                {"year": year}).fetchall()
        for book in books_found_at_year:
            print(f"Book published at {year} : {book.title} written by {book.author} in {book.year}.")
        if len(books) == 0:
            print("No books found.")

if __name__ == "__main__":
    main()
    app.run(debug=True) #  python3 application.py REPLACEs flask run

# set up the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    now = datetime.datetime.now()
    new_year = now.month == 1 and now.day == 1
    title = "bookees"
    headline = "Welcome to the booksite!"
    body = "Is today New Year ?"

    if session.get("reviews") is None:
        session["reviews"] = []

    if request.method == "POST":
        review = request.form.get("review")
        session["reviews"].append(review)
    return render_template("index.html", title=title, headline=headline, body=body, new_year=new_year, reviews = session["reviews"])

# to do: add description of this website in about.html
@app.route("/about")
def about():
    return "<h1>About Page</h1>"

# to do: user management section
@app.route("/user")
def user():
    return "User page"

# @app.route("/<string:name>")
# def hello(name):
#     name = name.capitalize()
#     return f"<h1>Hello, {name}</h1>"
