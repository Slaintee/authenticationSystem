import sys


def login():
    """Given user name and password,
    return message or main menu"""
    log_in = False
    MAX_TIME = 3
    incorrect_pw = 0
    while not log_in:
        # Open password table
        user_list = open("list.csv", "r")
        # Ask for user name and password input
        user_name = input("User name: ")
        password = str(input("Password: "))
        # Read user list
        for line in user_list:
            if line.split(',')[0] == user_name:
                if line.split(',')[1] == password:
                    log_in = True
                    access_level = line.split(',')[2]
        # Print mismatching message
        if not log_in:
            incorrect_pw += 1
            print("Incorrect user name or password.", MAX_TIME - incorrect_pw, "time(s) left.")
            if incorrect_pw == 3:
                print("Login failed. Exiting the system.")
                sys.exit()
        # Close list file
        user_list.close()
    # Print user level
    print("Welcome level " + access_level.rstrip() + " user " + user_name)
    # Return access level
    return int(access_level)


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
    choice = input("Return to the menu? (y/n) ")
    if choice == 'y':
        menu_area()
    elif choice == 'n':
        sys.exit()
    else:
        invalid()
        sys.exit()


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
    print("System logged out.")


def authentication():
    """Given user area choice, check user level
    and return whether validated or whether succeed"""
    # Ask login function for the access level
    access_level = login()
    # Call menu_area function
    menu_area()
    # Ask user choice as input
    try:
        choice = int(input("Requesting for menu area: "))

        # Authenticate level 1
        while access_level == 1:
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
        while access_level == 2:
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
        while access_level == 3:
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
        sys.exit()


def main():
    """Main function"""
    # Print head
    print("Welcome, enter the user name and password to log in thr system.")
    # Authenticate user
    authentication()


main()
