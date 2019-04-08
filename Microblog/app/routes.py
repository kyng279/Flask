from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) #redirects to main page if user already logged in
    form = LoginForm()
    if form.validate_on_submit(): #if all fields are valid
        user = User.query.filter_by(username=form.username.data).first() #retrieves user from database
        if user is None:
            user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):#failed log in attempt
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) #Log user in/ create user session
        next_page  = request.args.get('next') #parses url for next query string  argument
        if not next_page or url_parse(next_page).netloc != '': #.netloc checks if next argument is a local url. If not, we redirect to index (Security Measure)
            next_page = url_for('index')#sets next page to index if next query is empty or not relative
        return redirect(next_page) #redirect to next page after login
    return render_template('login.html', title='Sign In', form=form) #GET login form


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')#flask will accept any value for dynamic component <> and pass this as an argument to the view function
@login_required #restricts view function to logged in users
def user(username):# <username> in url is passed to the view function
    user = User.query.filter_by(username=username).first_or_404()#throws a 404 error if no user is found
    posts = [
        {'author': user, 'body':'Test post #1'},
        {'author': user, 'body':'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)