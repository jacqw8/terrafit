from flask import render_template, url_for, flash, redirect, request, send_from_directory, abort
from terrafit import app, db, bcrypt
from terrafit.forms import RegistrationForm, LoginForm, ReusableForm, AnotherForm
from terrafit.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from terrafit import donationfind
import os
from werkzeug.utils import secure_filename
from terrafit import keras


@app.route("/garden", methods=['GET', 'POST'])
@login_required
def home():
    form = AnotherForm()
    if form.validate_on_submit():
        num = int(form.number.data)
        arts = []
        for i in range(num):
            d = {}
            d['x'] = 'x'
            arts.append(d)
        return render_template('garden.html', title='Garden', arts=arts)
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

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route("/community")
@login_required
def community():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('community.html', title='Community', files=files)

@app.route('/community', methods=['POST'])
@login_required
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('community'))

@app.route('/clothes/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

# category = keras.which_one()
@app.route('/shop')
def shop():
    c = keras.main()
    files = []
    for i in range(len(c)):
        cwd = os.getcwd() + '/terrafit/ml_clothes/' + c[i]
        f = os.listdir(cwd)
        for j in range(len(f)):
            files.append(f[j])
    return render_template('shop.html', title='Shop', files=files)

@app.route('/shop', methods=['POST'])
@login_required
def upload_file2():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        cwd = os.getcwd() + '/terrafit/ml_clothes/new'
        uploaded_file.save(os.path.join(cwd, filename))
    return redirect(url_for('community'))

@app.route('/ml_clothes/new/<filename>')
def upload2(filename):
    cwd = os.getcwd() + '/terrafit/ml_clothes/new'
    return send_from_directory(cwd, filename)


@app.before_first_request
def create_tables():
    db.create_all()