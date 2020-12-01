"""
Lab 8
Ken Zhang
CS 166 / Fall 2020
"""

from datetime import datetime
import sqlite3


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


def get_date():
    """ Generate timestamp for data inserts """
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")


def add_user():
    """ Example data insert into users table """
    new_username = str(input("Please enter new username: "))  # Need exception handling
    new_password = str(input("Please enter new password: "))
    new_access = "1"
    data_to_insert = [(new_username, new_password,  new_access)]
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
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


def login():
    """Given user name and password,
    return message or main menu"""
    log_in = False
    MAX_TIME = 3
    incorrect_pw = 0
    try:
        while not log_in:
            conn = sqlite3.connect("user.db")
            c = conn.cursor()
            for row in c.execute("SELECT * FROM users"):
                user[row[0]] = {'password': row[1], 'access': row[2]}

            # Check if user is valid
            if user[username]['password'] == password:
                print('------- welcome, {} -------'.format(username))
                break
            else:
                # 3 times max if input incorrect
                incorrect_pw += 1
                print("Incorrect user name or password.", MAX_TIME - incorrect_pw, "time(s) left.")
                if incorrect_pw == 3:
                    print("Login failed. Exiting the system.")
                    exit()

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


if __name__ == "__main__":
    """Given user area choice, check user level
    and return whether validated or whether succeed"""
    # Print head
    print("Welcome, enter the user name and password to log in thr system.")
    # Authenticate user
    create_db()
    user = {}
    login_choice = 0
    while login_choice != 1 or login_choice != 2:
        try:
            login_choice = int(input("1. Log in\n2. Register\n->"))
            if login_choice == 1:
                print("------------ Login ------------")
                # Login
                username = input("Enter your username: ").strip()
                password = input("Enter your password: ").strip()
                break
            elif login_choice == 2:
                add_user()
                print("------------ Register ------------")
                # Register
                username = input("Create a username: ").strip()
                password = input("Creat a password: ").strip()
                break
            else:
                # avoid anything other than 1 and 2 entered
                invalid()
        except ValueError:
            # avoid anything other than number entered
            invalid()

    login()
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
