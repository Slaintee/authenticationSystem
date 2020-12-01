"""
Lab 8
Ken Zhang
CS 166 / Fall 2020
"""

from password_crack import hash_pw, authenticate
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


def add_user():
    """ Example data insert into users table """
    try:
        print("Do not enter quotation mark otherwise it will be removed.")
        new_username = str(input("Please enter new username: "))
        new_username = sql_injection(new_username)
        new_password = str(input("Please enter new password in length of between 8 and 25: "))
        while len(new_password) < 8 or len(new_password) > 25:
            new_password = str(input("Invalid length. Enter again: "))
        new_password = sql_injection(new_password)
        new_password = hash_pw(new_password)
        new_access = "1"
        data_to_insert = [(new_username, new_password, new_access)]
    except ValueError:
        invalid()
        exit()
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


def login(username, password):
    """Given user name and password,
    return message or main menu"""
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


def enter():
    max_time = 3
    logged_in = False
    while not logged_in:
        print("------------ Login ------------")
        username = input("Enter your username: ").strip()
        username = sql_injection(username)
        password = input("Enter your password: ").strip()
        password = sql_injection(password)
        logged_in = login(username, password)
        if logged_in:
            print('------- welcome, {} -------'.format(username))
            break
        else:
            max_time -= 1
            print("Incorrect user name or password.", max_time, "time(s) left.")
            if max_time == 0:
                print("Login failed. Exiting the system.")
                exit()
    return username


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
                # Login
                username = enter()
                break
            elif login_choice == 2:
                add_user()
                # Login
                username = enter()
                break
            else:
                # avoid anything other than 1 and 2 entered
                invalid()
        except ValueError:
            # avoid anything other than number entered
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
