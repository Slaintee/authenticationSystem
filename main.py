"""
Lab 8
Ken Zhang
CS 166 / Fall 2020
"""

from flask import Flask, redirect, url_for, render_template, flash, session, request
from flask_wtf import FlaskForm
from os import urandom
from password_crack import hash_pw, authenticate
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import random
import sqlite3
import string
import traceback


app = Flask(__name__)
app.config['SECRET_KEY'] = str(urandom(7))


# Register page's form group
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_password(self, password):
        """
        Check basic password strength. Return true if password
        meets minimum complexity criteria, false otherwise.

        :param self: str
        :param password: str
        """
        SPECIAL_CHAR = "!@#$%^&*"
        PASSWORD_MIN_LENGTH = 8
        PASSWORD_MAX_LENGTH = 25
        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Password should have at least one number")
        elif not any(char.isupper() for char in password.data):
            raise ValidationError("Password should have at least one uppercase")
        elif not any(char.islower() for char in password.data):
            raise ValidationError("Password should have at least one lowercase")
        elif not any(char in SPECIAL_CHAR for char in password.data):
            raise ValidationError("Password should have at least one special character (!@#$%^&*)")
        elif len(password.data) < PASSWORD_MIN_LENGTH or len(password.data) > PASSWORD_MAX_LENGTH:
            raise ValidationError("Password should have a length of between 8 and 25")


# Log in page's form group
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log In")


def create_db():
    """ Create table 'account_table' in 'account_data' database """
    try:
        conn = sqlite3.connect('account_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE account_table
                    (
                    username text,
                    password text,
                    level text
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def add_user(new_username, new_password):
    """ Insert new user into users table """
    # Set new user as least level
    new_level = "1"
    insert = [(new_username, new_password, new_level)]
    try:
        conn = sqlite3.connect('account_data.db')
        c = conn.cursor()
        # Insert new user to database
        c.executemany("INSERT INTO account_table VALUES (?, ?, ?)", insert)
        conn.commit()
    except sqlite3.IntegrityError:
        flash("Error. Tried to add duplicate record!", "danger")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def generate_password():
    """
    Generate a new random password satisfies the requirement

    :return: str
    """
    src = string.ascii_letters + string.digits + "!@#$%^&*"
    # Make random length of password
    num = random.randint(4, 21)
    # Choose num characters from src
    list_passwd_all = random.sample(src, num)
    # Make it includes digit
    list_passwd_all.extend(random.sample(string.digits, 1))
    # Make it includes lowercase
    list_passwd_all.extend(random.sample(string.ascii_lowercase, 1))
    # Make it includes uppercase
    list_passwd_all.extend(random.sample(string.ascii_uppercase, 1))
    # Make it includes special character
    list_passwd_all.extend(random.sample("!@#$%^&*", 1))
    # Shuffle the list and change it to string
    random.shuffle(list_passwd_all)
    str_passwd = ''.join(list_passwd_all)
    return str_passwd


@app.route("/", methods=["POST", "GET"])
def login():
    """
    Given user name and password,
    return message or main menu
    """
    form = LoginForm()
    # If click log in
    if form.validate_on_submit():
        try:
            # Get username and password
            username = sql_injection(form.username.data)
            password = sql_injection(form.password.data)
            conn = sqlite3.connect("account_data.db")
            c = conn.cursor()
            for row in c.execute("SELECT * FROM account_table"):
                account[row[0]] = {'password': row[1], 'level': row[2]}

            # Check if user is valid
            if authenticate(account[username]['password'], password):
                session.permanent = True
                session["user"] = username
                # Lead to the user page
                return redirect(url_for("user"))
            else:
                # 3 times max if input incorrect
                flash(f"Log in Failed", "danger")

        except sqlite3.DatabaseError:
            flash("Error. Could not retrieve data.", "danger")
        except KeyError:
            flash("Login Failed with KeyError.", "danger")
        finally:
            if c is not None:
                c.close()
            if conn is not None:
                conn.close()
    else:
        # Lead to user page if user is logged in
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """
    Log out from web
    """
    if "user" in session:
        user = session["user"]
        flash(f"{user} has logged out.", "success")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user():
    """User page"""
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    elif request.method == "POST":
        redirect(url_for("logout"))
    else:
        return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    """Register page"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a database if there is no database
        create_db()
        username = sql_injection(form.username.data)
        password = sql_injection(form.password.data)
        # Insert user to database
        add_user(username, hash_pw(password))
        flash(f'{form.username.data} has created!', "success")
        return redirect(url_for("login"))
    return render_template('register.html', form=form)


def sql_injection(value):
    """
    Stop user entering " to prevent sql injection

    :param value: str
    :return: str
    """
    if '"' in value:
        value = value.replace('"', '')
        return value
    else:
        return value


def enter(user):
    """
    Limit registered user has 3 times to log in.

    :param user:
    :return: str
    """
    # User has 3 times to enter the existing account
    max_time = 3
    logged_in = False
    while not logged_in:
        # Enter the username and password, and prevent from sql injection
        print("------------ Login ------------")
        username = input("Enter your username: ").strip()
        username = sql_injection(username)
        password = input("Enter your password: ").strip()
        password = sql_injection(password)
        logged_in = login(username, password, user)
        if logged_in:
            print('------- welcome, {} -------'.format(username))
            break
        else:
            # If account invalid more than 3 times, system out
            max_time -= 1
            print("Incorrect user name or password.", max_time, "time(s) left.")
            if max_time == 0:
                print("Login failed. Exiting the system.")
                exit()
    return username


if __name__ == "__main__":
    account = {}
    # pylint: disable=W0703
    try:
        app.run(debug=True, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()
