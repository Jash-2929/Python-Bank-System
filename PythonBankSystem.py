import os
import random
import hashlib
import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
    name TEXT,
    accid TEXT,
    mpin TEXT,
    loginpass TEXT,
    balance REAL,
    loginpass_salt TEXT,
    mpin_salt TEXT
)''')
conn.commit()

def hash_data(data, salt):
    return hashlib.sha256(data.encode() + bytes.fromhex(salt)).hexdigest()

def mpin_():
    print("Following are the choices for length of the MPIN.")
    print("1. 4-Digit MPIN")
    print("2. 6-Digit MPIN\n")
    while True:
        mpinchoice = input("Choose from the given options : ")
        if mpinchoice == "1":
            mpin = input("Enter your 4-Digit MPIN : ")
            if len(mpin) == 4 and mpin.isdigit():
                while True:
                    conf = input("Enter your MPIN again to confirm: ")
                    if conf == mpin:
                        return mpin
                    else:
                        print("MPIN does not match. Try again.")
            else:
                print("Please enter a valid MPIN.")
        elif mpinchoice == "2":
            mpin = input("Enter your 6-Digit MPIN : ")
            if len(mpin) == 6 and mpin.isdigit():
                while True:
                    conf = input("Enter your MPIN again to confirm: ")
                    if conf == mpin:
                        return mpin
                    else:
                        print("MPIN does not match. Try again.")
            else:
                print("Please enter a valid MPIN.")
        else:
            print("Please select from the given options only.")

def login_password():
    while True:
        password = input("Enter your Login Password : ")
        if 8 <= len(password) <= 12:
            has_alpha = any(char.isalpha() for char in password)
            has_digit = any(char.isdigit() for char in password)
            has_char = any(not char.isalnum() for char in password)

            if has_char and has_digit and has_alpha:
                print("The strength of your password is Strong")
                while True:
                    con = input("Enter your Login Password again to confirm : ")
                    if con == password:
                        return password
                    else:
                        print("The password does not match")
            elif (has_alpha and has_digit) or (has_char and has_digit) or (has_char and has_alpha):
                print("The strength of your password is Medium. Try again")
            else:
                print("The strength of your password is Weak. Try again")
        else:
            print("The password must contain 8 to 12 characters only. Try again.\n")

def input_float(prompt):
    while True:
        try:
            value=float(input(prompt))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return value

def input_int(prompt):
    while True:
        try:
            value=int(input(prompt))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return value

print("\n======================================")
print("     WELCOME TO PYTHON BANK SYSTEM     ")
print("======================================\n")

while True:
    print("========= MAIN MENU =========\n")
    print("1. Create New Account")
    print("2. Show All Accounts")
    print("3. Login to Account")
    print("4. Exit\n")
    option = input("Select an option : ")

    if option == "1":
        print("\n===== CREATE NEW ACCOUNT =====\n")

        name = input("Enter name for the new account: ")
        while not (name.replace(" ", "").isalpha() and not name.isspace()):
            print("Name can only contain alphabets and spaces, and cannot be only spaces.")
            name = input("Enter name for the new account: ")

        print("\n--- Create Login Password ---")
        print("You may enter alphabets, numbers or special characters.")
        print("The password must contain 8 to 12 characters only.\n")
        print("The password must contain an alphabet, a number and a special charater.\n")

        loginpass_salt = os.urandom(16).hex()
        loginpass = login_password()
        loginpass_hash = hash_data(loginpass, loginpass_salt)
        print("Your password has been created.")

        mpin_salt = os.urandom(16).hex()

        print("\n--- Create MPIN ---")
        mpin = mpin_()
        print("MPIN created successfully.")
        mpin_hash = hash_data(mpin, mpin_salt)

        while True:
            accid = "PBK" + str(random.randint(1000, 9999))
            cursor.execute("SELECT accid FROM accounts WHERE accid=?", (accid,))
            if not cursor.fetchone():
                break

        print("\nYour account ID is : ", accid)
        balance = input_float("Enter your starting balance : ")

        print("Congratulations! Your account has been created.\n")

        cursor.execute("INSERT INTO accounts VALUES (?,?,?,?,?,?,?)",
                       (name, accid, mpin_hash, loginpass_hash, balance, loginpass_salt, mpin_salt))
        conn.commit()

    elif option == "2":
        print("\n===== SHOW ALL ACCOUNTS =====\n")

        cursor.execute("SELECT name, accid FROM accounts")
        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts found.\n")
        else:
            print("--- List of All Accounts ---\n")
            for i, acc in enumerate(accounts, 1):
                print(f"{i}. {acc[0]} - {acc[1]}")
            print()

    elif option == "3":
        print("\n===== LOGIN =====\n")

        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts to login.\n")
        else:
            for i, acc in enumerate(accounts, 1):
                print(f"{i}. {acc[0]} - {acc[1]}")

            choice = input_int("\nChoose sr. number of account to login : ")

            if not (1 <= choice <= len(accounts)):
                print("Invalid choice\n")
            else:
                choice -= 1
                acc = accounts[choice]

                login_attempts = 3
                while login_attempts > 0:
                    loginpass = input("Enter Login Password : ")
                    if hash_data(loginpass, acc[5]) != acc[3]:
                        login_attempts -= 1
                        print(f"\nIncorrect Login Password. {login_attempts} attempts left.\n")
                    else:
                        print(f"\nWelcome {acc[0]}!\n")

                        deleted=False

                        while True:
                            print("===== ACCOUNT MENU =====\n")
                            print("1. View Account Details")
                            print("2. Withdraw")
                            print("3. Deposit")
                            print("4. Change MPIN")
                            print("5. Change Login Password")
                            print("6. Delete This Account")
                            print("7. Logout\n")

                            accopt = input("Choose an option: ")

                            cursor.execute("SELECT * FROM accounts WHERE accid=?", (acc[1],))
                            acc = cursor.fetchone()

                            if accopt == "1":
                                print("\n--- Account Details ---")
                                print(f"Name       : {acc[0]}")
                                print(f"Account ID : {acc[1]}")
                                print(f"Balance    : {acc[4]}\n")

                            elif accopt == "2":
                                print("\n--- Withdraw ---")
                                amount = input_float("Enter amount to withdraw : ")
                                attempts=3
                                while attempts>0:
                                    pin = input("Enter your MPIN : ")
                                    if hash_data(pin, acc[6]) == acc[2]:
                                        if amount <= acc[4] and amount>0:
                                            new_balance = acc[4] - amount
                                            cursor.execute("UPDATE accounts SET balance=? WHERE accid=?", (new_balance, acc[1]))
                                            conn.commit()
                                            print("Withdrawal successful. Your new balance is : ", new_balance)
                                            break
                                        else:
                                            print("Insufficient balance. Returning to account menu...")
                                            break
                                    else:
                                        attempts-=1
                                        print(f"\nIncorrect MPIN. {attempts} attempts left.")
                                if attempts==0:
                                    print("Too many failed attempts. Returning to account menu...")
                                    continue

                            elif accopt == "3":
                                print("\n--- Deposit ---")
                                amount = input_float("Enter amount to deposit : ")
                                attempts=3
                                while attempts>0:
                                    pin = input("Enter your MPIN : ")
                                    if hash_data(pin, acc[6]) == acc[2]:
                                        if amount > 0:
                                            new_balance = acc[4] + amount
                                            cursor.execute("UPDATE accounts SET balance=? WHERE accid=?", (new_balance, acc[1]))
                                            conn.commit()
                                            print("Deposit successful. Your new balance is : ", new_balance)
                                            break
                                        else:
                                            print("Please enter an amount greater than 0. Returning to account menu...")
                                            break
                                    else:
                                        attempts-=1
                                        print(f"\nIncorrect MPIN. {attempts} attempts left.")
                                if attempts==0:
                                    print("Too many failed attempts. Returning to account menu...")
                                    continue

                            elif accopt == "4":
                                print("\n--- Change MPIN ---")
                                attempts=3
                                while attempts>0:
                                    pin = input("Enter your current MPIN : ")
                                    if hash_data(pin, acc[6]) == acc[2]:
                                        new_salt = os.urandom(16).hex()
                                        newmpin = mpin_()
                                        print("MPIN changed successfully.")
                                        newmpin = hash_data(newmpin,new_salt)
                                        cursor.execute("UPDATE accounts SET mpin=?, mpin_salt=? WHERE accid=?", (newmpin, new_salt, acc[1]))
                                        conn.commit()
                                        break
                                    else:
                                        attempts-=1
                                        print(f"\nIncorrect MPIN. {attempts} attempts left.")
                                if attempts==0:
                                    print("Too many failed attempts. Returning to account menu...")
                                    continue

                            elif accopt == "5":
                                print("\n--- Change Login Password ---")
                                attempts=3
                                while attempts>0:
                                    login = input("\nEnter your current Login Password : ")
                                    if hash_data(login, acc[5]) == acc[3]:
                                        print("\nYou may enter alphabets, numbers or special characters.")
                                        print("The password must contain 8 to 12 characters only.")
                                        print("The password must contain an alphabet, a number and a special character.")
                                        new_salt = os.urandom(16).hex()
                                        loginpass = login_password()
                                        loginpass = hash_data(loginpass,new_salt)
                                        cursor.execute("UPDATE accounts SET loginpass=?, loginpass_salt=? WHERE accid=?", (loginpass, new_salt, acc[1]))
                                        conn.commit()
                                        print("\nLogin Password changed successfully.")
                                        break
                                    else:
                                        attempts-=1
                                        print(f"\nIncorrect Login Password. {attempts} attempts left.")
                                if attempts==0:
                                    print("Too many failed attempts. Returning to account menu.")
                                    continue

                            elif accopt == "6":
                                print("\n--- Delete Account ---")
                                attempts=3
                                while attempts>0:
                                    pin = input("\nEnter your MPIN : ")
                                    if hash_data(pin, acc[6]) == acc[2]:
                                        break
                                    else:
                                        attempts-=1
                                        print(f"Incorrect MPIN. {attempts} attempts left.\n")
                                        print("Account not deleted.\n")
                                if attempts==0:
                                    print("Too many failed attempts. Returning to account menu...")
                                    continue

                                attempts=3
                                while attempts>0:
                                    login = input("Enter your Login Password : ")
                                    if hash_data(login, acc[5]) == acc[3]:
                                        confirm = input("\nAre you sure you want to delete this account? (y/n): ").lower()
                                        if confirm in ("y","yes"):
                                            cursor.execute("DELETE FROM accounts WHERE accid=?", (acc[1],))
                                            conn.commit()
                                            print("Account", acc[0], "deleted.\n")
                                            deleted=True
                                            break
                                        elif confirm in ("n","no"):
                                            print("Cancelled")
                                            break
                                        else:
                                            print("Invalid input")
                                    else:
                                        attempts-=1
                                        print(f"Incorrect Login Password. {attempts} attempts left.\n")
                                if deleted:
                                    break
                                if attempts==0:
                                    print("Too many failed attempts. Returning to account menu...")
                                else:
                                    continue

                            elif accopt == "7":
                                print("\nThank you for using the Python Bank System. Logging out...\n")
                                break

                            else:
                                print("Invalid option. Try again.\n")
                        break
                if login_attempts == 0:
                    print("Too many failed attempts. Returning to main menu...\n")
                    continue
                continue

    elif option == "4":
        print("\nThank you for using the Python Bank System. Goodbye!\n")
        break

    else:
        print("\nInvalid option. Try again.\n")
