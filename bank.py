"""
Catamount Community Bank
Flask Routes

Warning: This app contains deliberate security vulnerabilities
Do not use in a production environment! It is provided for security
training purposes only!

"""

import csv
from config import display
from flask import Flask, render_template, request, url_for, flash, redirect
from db import Db
from lessons import sql_injection
from lessons.password_crack import hash_pw, authenticate

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')


@app.route("/", methods=['GET', 'POST'])
def home():
    """Login the user. TODO """
    query_term = ''
    with open(app.config['CREDENTIALS_FILE']) as fh:
        reader = csv.DictReader(fh)
        credentials = {row['username']:
                            {'acct_id': row['id'],
                             'pw_hash': row['password_hash']}
                       for row in reader}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pw_hash = hash_pw(password)
        query_term = request.form.get('query_term')
        q = sql_injection.query(query_term)
        try:
            if authenticate(pw_hash, password):
                return redirect(url_for('login_success',
                                        id_=credentials[username]['acct_id']))
        except KeyError:
            pass
        flash("Invalid username or password!", 'alert-danger')
    return render_template('home.html',
                           query_term=query_term,
                           query=q,
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/login_success/<int:id_>", methods=['GET', ])
def login_success(id_):
    flash("Welcome! You have logged in!", 'alert-success')
    return render_template('customer_home.html',
                           title="Customer Home",
                           heading="Customer Home")


@app.route("/hashit", methods=['GET', ])
def hashit():
    """Hash a password. DON'T EVER DO THIS LIKE THIS IN THE REAL WORLD! """
    pw = request.args.get('pw')
    salt = request.args.get('salt')
    if salt is None:
        salt = ''
    return hash_pw(pw, salt)
