from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskarticles import  db, bcrypt
from flaskarticles.Models.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskarticles.blueprints.Users.forms import RegistrationForm, LoginForm
from flaskarticles.utils import docache

users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are able to log in', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
# @docache(minutes=3, content_type='home.html')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # check if user exits and compare passwords
        if user and bcrypt.check_password_hash(user.password, form.password.data): # compare the password from database and the password from the form that user entered
            login_user(user)                # log user in
            flash('Your have logged in successfully', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful. Please check Email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


# when clicking on username, a nwe page will show up with their articles posted
@users.route("/user/<string:username>")
@docache(minutes=3, content_type='userarticles.html')
def user_articles(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404() # filter on username
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) # pagination with default page =1, 5 number of pages per page, sort descinding so the last arrticles show up first
    return render_template('userarticles.html', posts=posts, user=user)
