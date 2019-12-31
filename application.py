import os,datetime, csv

from flask import Flask,render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def main():
    # As long as import.py run once, the following is not needed.
    # b = open("books_test.csv")
    # reader = csv.reader(b) # read b as csv file

    # for isbn, title, author, year in reader:
    #     db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
    #     {"isbn": isbn, "title": title, "author": author, "year": year})
    #     print(f"Added book title is: {title} written by {author} in {year}.")

    books = db.execute("select * from books where year=1998;").fetchall()
    for book in books:
        print(f"Book found: title : {book.title} written by {book.author} in {book.year}.")

    db.commit()

if __name__ == "__main__":
    main()

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
    index_page = render_template("index.html", title=title, headline=headline, body=body, new_year=new_year, reviews = session["reviews"])
    return index_page

@app.route("/user")
def user():
    return "User page"

# @app.route("/<string:name>")
# def hello(name):
#     name = name.capitalize()
#     return f"<h1>Hello, {name}</h1>"
