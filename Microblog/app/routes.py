from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) #redirects to main page if user already logged in
    form = LoginForm()
    if form.validate_on_submit(): #if all fields are valid
        user = User.query.filter_by(username=form.username.data).first() #retrieves user from database
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

