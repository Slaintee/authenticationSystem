"""
Lab 8
Ken Zhang
CS 166 / Fall 2020
"""

from authentication import password_strength
from config import display
import csv
from flask import Flask, render_template, request, url_for, flash, redirect
from db import Db
from password_crack import hash_pw, authenticate
import random
import sqlite3
import string

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')


def create_db():
    """ Create table 'users' in 'user' database """
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                    (
                    username text,
                    password text,
                    access text
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


def add_user(user):
    """ Insert new user into users table """
    try:
        print("Do not enter quotation mark otherwise it will be removed.")
        # Ask for new username and password, and prevent from sql injection
        new_username = str(input("Please enter new username: "))
        new_username = sql_injection(new_username)
        new_password = str(input("Please enter new password in length of between 8 and 25, \n"
                                 "and have at least one number, at least one lowercase letter, \n"
                                 "at least one uppercase letter, and at at least one special character(!@#$%^&*) \n"
                                 "in the password: "))
        while not password_strength(new_password):
            new_password = str(input("Invalid input. Enter again: "))
        new_password = sql_injection(new_password)
        new_password = hash_pw(new_password)
        # Set new user as least level
        new_access = "1"
        data_to_insert = [(new_username, new_password, new_access)]
    except ValueError:
        invalid()
        exit()
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        # Insert new user to database
        c.executemany("INSERT INTO users VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
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


def login(username, password, user):
    """
    Given user name and password,
    return message or main menu

    :param username: str
    :param password: str
    """
    try:
        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users"):
            user[row[0]] = {'password': row[1], 'access': row[2]}

        # Check if user is valid
        if authenticate(user[username]['password'], password):
            logged_in = True
        else:
            # 3 times max if input incorrect
            logged_in = False
        return logged_in

    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    except KeyError:
        # using invalid username will terminate the program
        print("{} is not a valid username".format(username))
        exit()
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def menu_area():
    """Return different options for user choice"""
    print("Press 1 for Time Reporting area")
    print("Press 2 for Accounting area")
    print("Press 3 for IT Helpdesk area")
    print("Press 4 for Engineering Documents area")
    print("Press 5 for Log out")


def not_authorized():
    """Return output if user is not authorized for this area"""
    print(" ")
    print("You are not authorized to access this area.")
    menu_choice = input("Return to the menu? (y/n) ")
    if menu_choice == 'y':
        menu_area()
    elif menu_choice == 'n':
        exit()
    else:
        invalid()
        exit()


def time_reporting():
    """Return output if user is authorized for this area"""
    print(" ")
    print("You have now accessed the Time Reporting area.")


def accounting():
    """Return output if user is authorized for this area"""
    print(" ")
    print("You have now accessed the accounting area.")


def it_helpdesk():
    """Return output if user is authorized for this area"""
    print(" ")
    print("You have now accessed the IT Helpdesk area.")


def engineering_documents():
    """Return output if user is authorized for this area"""
    print(" ")
    print("You have now accessed the Engineering Documents area.")


def logout():
    """Return output if system is logged out"""
    print(" ")
    print("System logged out.")


def invalid():
    """Return output if input is invalid"""
    print(" ")
    print("Invalid input")


def sql_injection(value):
    if '"' in value:
        value = value.replace('"', '')
    return value


def enter(user):
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


# @app.route("/", methods=['GET', 'POST'])
def home():
    """Given user area choice, check user level
    and return whether validated or whether succeed"""

    # Authenticate user
    create_db()
    user = {}
    login_choice = 0

    while login_choice != 1 or login_choice != 2:
        try:
            login_choice = int(input("1. Log in\n2. Register\n->"))
            if login_choice == 1:
                # Login
                username = enter(user)
                break
            elif login_choice == 2:
                add_user(user)
                # Login
                username = enter(user)
                break
            else:
                # Stop entering anything other than 1 and 2
                invalid()
        except ValueError:
            # Stop entering anything other than number
            invalid()

    # Ask login function for the access level
    access_level = user[username]['access']
    # Call menu_area function
    menu_area()
    # Ask user choice as input
    try:
        choice = int(input("Requesting for menu area: "))

        # Authenticate level 1
        while access_level == '1':
            if choice == 1:
                time_reporting()
                break
            elif choice == 2 or choice == 3 or choice == 4:
                not_authorized()
                choice = int(input("Requesting for menu area: "))
            elif choice == 5:
                logout()
                break
            else:
                invalid()
                break

        # Authenticate level 2
        while access_level == '2':
            if choice == 1:
                time_reporting()
                break
            if choice == 2:
                accounting()
                break
            elif choice == 3:
                it_helpdesk()
                break
            elif choice == 5:
                logout()
                break
            else:
                invalid()
                break

        # Authenticate level 3
        while access_level == '3':
            if choice == 1:
                time_reporting()
                break
            if choice == 2:
                accounting()
                break
            elif choice == 3:
                it_helpdesk()
                break
            elif choice == 4:
                engineering_documents()
                break
            elif choice == 5:
                logout()
                break
            else:
                invalid()
                break
    # Catch ValueError
    except ValueError:
        invalid()
        exit()


home()
