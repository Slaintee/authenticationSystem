# authenticationSystem
by Ken Zhang, CS166, Lab 8

### Description
The project is an user system to register and log in.

### Set up
Install flask and flask-WTF on the computer.
- In ternimal, `pip install flask` and `pip install flask-WTF`, or use pip3
- In IDE like PyCharm, find Preference -> Python Interpreter -> install

### Run
- To run the project, just run `main.py`.
- Click the link showed in window, or copy this path `http://localhost:8097/`, it will lead to the log in page.
- If you don't have account, click the Register button, you will go to register page. 
But you can also use the prepared account:
   - username: `alpha`
   - password: `Alpha123!`
   - level: `3` (highest)
- In register page, enter the username and password. Password should have:
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number
   - At least one special character in `!@#$%^&*`
   - Length of between 8 and 25
   - The program will drop the quotation marks from textbox to prevent sql injection.
   - New user will have a least level, 1.
   - I have created `generate_password()` function in `main.py`, but I'm still trying to figure out how to implement it. 
   Or you can use right click the password textbox to generate a password.
- There will be a message to let you know whether you successfully registered. If so, you will be lead to log in page.
- Enter the correct username and password to log in.
   - I have created `enter()` function, which is limiting the user with 3 times maximum of entering wrong password, 
   in `main.py`, but I'm still trying to figure out how to implement it. 
- You will be lead to user page if you logged in successfully.