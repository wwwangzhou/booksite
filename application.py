import os,datetime, csv

from flask import Flask,render_template, session, request, url_for, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LoginForm

# bridge the connection between Python and Database
engine = create_engine(os.getenv("DATABASE_URL"))

# allow each user have her/his own workspace
db = scoped_session(sessionmaker(bind=engine))

# create an instance of Flask class
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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

# Dummy reviews
posts = [
    {
        'user_name': 'Corey Schafer',
        'book_title': 'The Gangester we are looking for',
        'comment': "I don't know how time moves or which of our sorrows or our desires it is able to wash away.",
        'date_reviewed': 'Dec 31, 2019',
        'rating': '5'
    },
    {
        'user_name': 'Jane Doe',
        'book_title': 'Into the wild',
        'comment': "You really should make a radical change in your lifestyle and begin to boldly do things which you may previously never have thought of doing, or been too hesitant to attempt. So many people live within unhappy circumstances and yet will not take the initiative to change their situation because they are conditioned to a life of security, conformity, and conservatism, all of which may appear to give one peace of mind, but in reality nothing is more damaging to the adventurous spirit within a man than a secure future. The very basic core of a man's living spirit is his passion for adventure. The joy of life comes from our encounters with new experiences, and hence there is no greater joy than to have an endlessly changing horizon, for each day to have a new and different sun.",
        'date_reviewed': 'Jan 1, 2020',
        'rating': '5'
    }
]

if __name__ == "__main__":
    main()
    app.run(debug=True) #  python3 application.py REPLACEs flask run

# set up the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    title = "bookees"
    headline = "Welcome to the booksite!"

    # intialize only once when making get request for the first time
    if session.get("reviews") is None:
        session["reviews"] = []

    # process post request: either add new or ignore duplicate entry
    if request.method == "POST":
        review = request.form.get("review")
        if review not in session["reviews"]:
            session["reviews"].append(review)

    # render the hompage index.html
    return render_template("index.html", title=title, headline=headline, posts=posts, reviews = session["reviews"])

# to do: add description of this website in about.html
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # generate one time alert
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'zouwang@ucdavis.edu' and form.password.data == 'wang':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# to do: user management section
@app.route("/user")
def user():
    return "User page"

# @app.route("/<string:name>")
# def hello(name):
#     name = name.capitalize()
#     return f"<h1>Hello, {name}</h1>"
