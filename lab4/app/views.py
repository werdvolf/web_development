from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from os import path
import mimetypes
import sqlite3


CUR_PATH = path.dirname(path.abspath(__file__))
# The directory with all web-related templates.
template_dir = path.join(CUR_PATH, "../templates")
# The directory for static files, such as .css, client-side JavaScript.
static_dir = path.join(CUR_PATH, "../static")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/html", ".html")
database_path = path.join(CUR_PATH, "../database")


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route("/order-page")
def order():
    return render_template("order.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


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
    return render_template('registration.html', form=form)


@app.route("/api/v1/order/make_order", methods=["GET", "POST"])
def make_order():
    orders_db_fn = "orders.db"

    orders_db_fp = path.join(database_path, orders_db_fn)
    order_db = sqlite3.connect(orders_db_fp)
    desc = request.args.get('description')
    cn = request.args.get('company_name')
    mb = request.args.get('min_budget')
    if desc is None or len(desc) == 0:
        desc = "NULL"
    sql = '''
    INSERT INTO orders
    (company_name, min_budget, max_budget, media_ad_type, outdoor_ad_type, product_placement_ad_type, tv_ad_type, radio_ad_type, description_ad_type)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    task = (
        request.args.get('company_name'),
        request.args.get('min_budget'),
        request.args.get('max_budget'),
        request.args.get('media'),
        request.args.get('outdoor'),
        request.args.get('product_placement'),
        request.args.get('tv'),
        request.args.get('radio'),
        desc
    )
    order_db_cursor = order_db.cursor()
    order_db_cursor.execute(sql, task)
    order_db.commit()

    return dict({"data": "Everything is fine"})
