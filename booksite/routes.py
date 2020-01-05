from flask import render_template, session, request, url_for, flash, redirect
from booksite import app, db, bcrypt
from booksite.forms import RegistrationForm, LoginForm
from booksite.models import User, Post

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
    if form.validate_on_submit(): # if valid, hash ps and save it to database db
        # generate one time alert.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
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
