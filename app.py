# Contributer Azim Mustufa Baldiwala, Github: github.com/azimbaldiwala
import getpass
from typing import ContextManager
import pyperclip as cp 
from Crypto.Cipher import AES 
import database
from AES import encrypt
from AES import decrypt
import secrets
import string  
from tabulate import tabulate as tb


displayMenu = """   
    AES ENCRYPTED PASSWORD MANAGER
    1. Login --> 1
    2. Sign-up --> 2
    3. Exit  --> exit()
"""


while True:
    print(displayMenu)
    user_input = input("Enter any option: ")
    if user_input == 'exit()':
        break 

    # Login Block.
    if user_input == '1':
        username = input("Enter your username: ")
        password = getpass.getpass()
        if database.validate_login(username, password):
            print("You are logged-in to the application!")

            
            # Next user-menu
            loginUsername = username
            menu = """
                1. Save New password
                2. Copy a password
                3. view password titles
                4. Change a password 
                5. delete old password
                6. exit
            """
            print(menu)
            opt = input("Enter any option: ")

            if opt == '4':
                break
            
            if opt == '1':
                password_for = input("Enter title for the password: ")      # Asking user for credentials.
                password = getpass.getpass()
                key = input("Please enter your AES encryption key[Given at the time of sign-up]: ")
                if password_for == None or password == None or len(key) < 8:        # Encryption constraint.
                    print("password & title cannot be None and len of key should not be less than 8")
                    continue
                # Encrypting the password.
                enc_pass = encrypt(password, key)
                database.insert_new_password(loginUsername, password_for, enc_pass)
                print("New password saved!")
            
            if opt == '2':
                get_name = input("Enter the title: ")

                if not database.check_title(get_name, loginUsername):
                    print("No password was saved for: ", get_name)
                    continue

                get_key = input("Enter the decryption key[Same key with which the password was encrypted]: ")
                password = database.get_pass(loginUsername, get_name)
                result = decrypt(password[0][0], get_key)
                cp.copy(str(result))
                print("Password copied to the clipboard.")
                continue
            
            if opt =='3':
                data = database.show_titles(loginUsername)
                print(tb(data))
                continue

            if opt == '4':
                pass_title = input("Enter the title of the password: ")
                if not database.check_title(pass_title, loginUsername):
                    print("No password was saved for: " +  get_name)
                    continue
                new_pass = input("Enter new password for " +  pass_title +  " : ")
                key = input("Please enter your AES encryption key[Given at the time of sign-up]: ")
                if password_for == None or password == None or len(key) < 8:
                    print("password & title cannot be None and len of key should not be less than 8")
                    continue
                # Encrypting the password.
                enc_pass = encrypt(password, key)
                database.update_pass(loginUsername, pass_title, enc_pass)
                print("Your password was updated!")
                continue

            if opt == '5':
                pass_title = input("Enter the title of the password: ")
                if not database.check_title(pass_title):
                    print("No such title found!")
                    continue

                con = input("Are you sure you want to delete the record with title " + pass_title + "(y/n): ")
                if con == 'y' or con == 'Y':
                    database.delete_password(loginUsername, pass_title)
                    print("Recored deleted!")
                    continue    
                print("Operation cancled.")
                continue

            else: 
                print("Please enter a valid option!")
                continue

        else:
            print("Enter  valid login credentials!")
            continue


    # Sign-up block
    if user_input == '2':
        username = input("Enter a unique username: ")
        if not database.check_username(username):
            print("Username already exist!")
            continue
        print("Enter the password(not less than 8 characters): ")
        password = getpass.getpass()
        if len(password) <= 8:
            print("Make a stronger password.")
            continue
        database.signup(username, password)
        print("New user added!")
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(8))
        print("Your 8 digit encryption key is: ", res )
        print("we highly recommend you to use the same for encryting and decrypting your passwords.")
