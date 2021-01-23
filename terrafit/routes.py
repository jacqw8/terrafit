from flask import render_template, url_for, flash, redirect, request
from terrafit import app, db, bcrypt
from terrafit.forms import RegistrationForm, LoginForm, ReusableForm, AnotherForm
from terrafit.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from terrafit import donationfind


posts = [
    {
        'author': 'Jackie Wu',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/garden", methods=['GET', 'POST'])
@login_required
def home():
    form = AnotherForm()
    if form.validate_on_submit():
        num = form.number.data
        return render_template('garden.html', title='Garden')
    return render_template('flowers.html', title='Garden', form=form) # can add argument

@app.route("/guides")
def about():
    return render_template('guides.html', title='Guides')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
        return redirect(url_for('map'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('map'))
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

@app.route("/index")
def index():
    return render_template('index.html', title='Index')

@app.route("/map", methods=['GET', 'POST'])
def map():
    form = ReusableForm()
    if form.validate_on_submit():
        clothes = donationfind.get_places(form.zipcode.data)
        return render_template('zip.html', clothes=clothes)
    return render_template('map.html', title='Map', form=form)

@app.before_first_request
def create_tables():
    db.create_all()