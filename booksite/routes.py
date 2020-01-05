import os
import secrets
from PIL import Image
from flask import render_template, session, request, url_for, flash, redirect, request, abort
from booksite import app, db, bcrypt
from booksite.forms import RegistrationForm, LoginForm, PostForm
from booksite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Dummy reviews
# posts = [
#     {
#         'user_name': 'Corey Schafer',
#         'book_title': 'The Gangester we are looking for',
#         'comment': "I don't know how time moves or which of our sorrows or our desires it is able to wash away.",
#         'date_reviewed': 'Dec 31, 2019',
#         'rating': '5'
#     },
#     {
#         'user_name': 'Jane Doe',
#         'book_title': 'Into the wild',
#         'comment': "You really should make a radical change in your lifestyle and begin to boldly do things which you may previously never have thought of doing, or been too hesitant to attempt. So many people live within unhappy circumstances and yet will not take the initiative to change their situation because they are conditioned to a life of security, conformity, and conservatism, all of which may appear to give one peace of mind, but in reality nothing is more damaging to the adventurous spirit within a man than a secure future. The very basic core of a man's living spirit is his passion for adventure. The joy of life comes from our encounters with new experiences, and hence there is no greater joy than to have an endlessly changing horizon, for each day to have a new and different sun.",
#         'date_reviewed': 'Jan 1, 2020',
#         'rating': '5'
#     }
# ]

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
    posts=Post.query.all()

    # render the hompage index.html
    return render_template("index.html", title=title, headline=headline, posts=posts, reviews = session["reviews"])

# to do: add description of this website in about.html
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # database query for matching user if there is
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/user")
def user():
    return "User page"

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # give the post with the given id
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # give the post with the given id
    if post.author != current_user: # to do 让管理员也可以修改
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
