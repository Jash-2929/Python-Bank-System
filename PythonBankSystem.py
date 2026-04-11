import os
import random
import hashlib
import sqlite3
import time

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
    name TEXT,
    accid TEXT,
    mpin TEXT,
    loginpass TEXT,
    balance REAL,
    loginpass_salt TEXT,
    mpin_salt TEXT,
    temp_lock_until REAL,
    perm_lock INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    accid TEXT,
    type TEXT,
    amount REAL,
    other TEXT,
    time TEXT,
    balance REAL
)''')

conn.commit()


def hash_data(data, salt):
    return hashlib.sha256(data.encode() + bytes.fromhex(salt)).hexdigest()


def log_transaction(accid, ttype, amount, balance, other=""):
    cursor.execute("INSERT INTO transactions VALUES (?,?,?,?,datetime('now','localtime'),?)",
                   (accid, ttype, amount, other, balance))
    conn.commit()


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
        password = input("Enter your new Login Password : ")
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
            return float(input(prompt))
        except:
            print("Invalid input. Please enter a valid number.")


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except:
            print("Invalid input. Please enter a valid number.")


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

        cursor.execute("INSERT INTO accounts VALUES (?,?,?,?,?,?,?,0,0)",
                       (name, accid, mpin_hash, loginpass_hash, balance, loginpass_salt, mpin_salt))

        log_transaction(accid, "Starting Balance", balance, balance)

        conn.commit()

    elif option == "2":
        print("\n===== SHOW ALL ACCOUNTS =====\n")

        cursor.execute("SELECT name, accid FROM accounts")
        data = cursor.fetchall()

        if not data:
            print("No accounts found.\n")
        else:
            print("--- List of All Accounts ---\n")
            for i, acc in enumerate(data, 1):
                print(f"{i}. {acc[0]} - {acc[1]}")
            print()

    elif option == "3":
        print("\n===== LOGIN =====\n")

        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts to login.\n")
            continue

        for i, acc in enumerate(accounts, 1):
            print(f"{i}. {acc[0]} - {acc[1]}")

        choice = input_int("\nChoose sr. number of account to login : ")

        if not (1 <= choice <= len(accounts)):
            print("Invalid choice\n")
            continue

        acc = accounts[choice - 1]

        if acc[8] == 1:
            print("\nAccount is permanently locked.")
            print("Recover your account by resetting credentials.\n")

            newpass = login_password()
            newpin = mpin_()

            new_salt1 = os.urandom(16).hex()
            new_salt2 = os.urandom(16).hex()

            cursor.execute("UPDATE accounts SET loginpass=?, mpin=?, loginpass_salt=?, mpin_salt=?, perm_lock=0 WHERE accid=?",
                           (hash_data(newpass, new_salt1), hash_data(newpin, new_salt2), new_salt1, new_salt2, acc[1]))
            conn.commit()

            print("Account recovered successfully.\n")
            continue

        if acc[7] > time.time():
            remain = int(acc[7] - time.time())
            print(f"\nAccount temporarily locked. Try again in {remain} seconds.\n")
            continue

        attempts = 3
        while attempts > 0:
            lp = input("Enter Login Password : ")
            if hash_data(lp, acc[5]) != acc[3]:
                attempts -= 1
                print(f"\nIncorrect Login Password. {attempts} attempts left.\n")
            else:
                break

        if attempts == 0:
            cursor.execute("UPDATE accounts SET perm_lock=1 WHERE accid=?", (acc[1],))
            conn.commit()
            print("Too many attempts. Account permanently locked.\n")
            continue

        print(f"\nWelcome {acc[0]}!\n")

        while True:
            print("===== ACCOUNT MENU =====\n")
            print("1. View Account Details")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer Money")
            print("5. Transaction History")
            print("6. Change MPIN")
            print("7. Change Login Password")
            print("8. Delete This Account")
            print("9. Logout\n")

            opt = input("Choose an option: ")

            cursor.execute("SELECT * FROM accounts WHERE accid=?", (acc[1],))
            acc = cursor.fetchone()

            if acc[8] == 1:
                print("Account permanently locked. Logging out.\n")
                break

            if opt == "1":
                print("\n--- Account Details ---")
                print(f"Name       : {acc[0]}")
                print(f"Account ID : {acc[1]}")
                print(f"Balance    : {acc[4]}\n")

            elif opt == "2":
                print("\n--- Withdraw ---")
                amt = input_float("Enter amount to withdraw : ")
                a = 3
                while a > 0:
                    pin = input("Enter your MPIN : ")
                    if hash_data(pin, acc[6]) == acc[2]:
                        if 0 < amt <= acc[4]:
                            nb = acc[4] - amt
                            cursor.execute("UPDATE accounts SET balance=? WHERE accid=?", (nb, acc[1]))
                            log_transaction(acc[1], "Withdraw", amt, nb)
                            conn.commit()
                            print("Withdrawal successful. Your new balance is : ", nb)
                            break
                        else:
                            print("Insufficient balance. Returning to account menu...")
                            break
                    else:
                        a -= 1
                        print(f"\nIncorrect MPIN. {a} attempts left.")
                if a == 0:
                    print("Too many failed attempts. Returning to account menu...\n")

            elif opt == "3":
                print("\n--- Deposit ---")
                amt = input_float("Enter amount to deposit : ")
                a = 3
                while a > 0:
                    pin = input("Enter your MPIN : ")
                    if hash_data(pin, acc[6]) == acc[2]:
                        if amt > 0:
                            nb = acc[4] + amt
                            cursor.execute("UPDATE accounts SET balance=? WHERE accid=?", (nb, acc[1]))
                            log_transaction(acc[1], "Deposit", amt, nb)
                            conn.commit()
                            print("Deposit successful. Your new balance is : ", nb)
                            break
                        else:
                            print("Invalid amount. Returning to account menu...")
                            break
                    else:
                        a -= 1
                        print(f"\nIncorrect MPIN. {a} attempts left.")
                if a == 0:
                    print("Too many failed attempts. Returning to account menu...\n")

            elif opt == "4":
                print("\n--- Transfer Money ---")
                to = input("Enter receiver Account ID : ")
                cursor.execute("SELECT * FROM accounts WHERE accid=?", (to,))
                rec = cursor.fetchone()

                if not rec:
                    print("Account not found.\n")
                    continue

                amt = input_float("Enter amount to transfer : ")

                a = 3
                while a > 0:
                    pin = input("Enter your MPIN : ")
                    if hash_data(pin, acc[6]) == acc[2]:
                        if amt > acc[4]:
                            print("Insufficient balance.\n")
                            break
                        if amt <= 0:
                            print("Invalid amount.\n")
                            break

                        cursor.execute("UPDATE accounts SET balance=? WHERE accid=?", (acc[4] - amt, acc[1]))
                        cursor.execute("UPDATE accounts SET balance=? WHERE accid=?", (rec[4] + amt, rec[1]))

                        log_transaction(acc[1], "Transfer Sent", amt, acc[4] - amt, rec[1])
                        log_transaction(rec[1], "Transfer Received", amt, rec[4] + amt, acc[1])

                        conn.commit()

                        print("Transfer successful.\n")
                        break
                    else:
                        a -= 1
                        print(f"\nIncorrect MPIN. {a} attempts left.")

                if a == 0:
                    print("Too many failed attempts.\n")

            elif opt == "5":
                print("\n--- Transaction History ---\n")

                cursor.execute("SELECT * FROM transactions WHERE accid=?", (acc[1],))
                rows = cursor.fetchall()

                print(f"{'TYPE':<20}{'AMOUNT':<10}{'OTHER':<15}{'BALANCE':<12}{'TIME':<20}")
                print("-" * 77)

                for r in rows:
                    print(f"{r[1]:<20}{r[2]:<10}{r[3]:<15}{r[5]:<12}{r[4]:<20}")
                print()

            elif opt == "6":
                print("\n--- Change MPIN ---")
                a = 3
                while a > 0:
                    pin = input("Enter your current MPIN : ")
                    if hash_data(pin, acc[6]) == acc[2]:
                        new_salt = os.urandom(16).hex()
                        newmpin = mpin_()
                        print("MPIN changed successfully.")
                        cursor.execute("UPDATE accounts SET mpin=?, mpin_salt=? WHERE accid=?",
                                       (hash_data(newmpin, new_salt), new_salt, acc[1]))
                        conn.commit()
                        break
                    else:
                        a -= 1
                        print(f"\nIncorrect MPIN. {a} attempts left.")
                if a == 0:
                    print("Too many failed attempts.\n")

            elif opt == "7":
                print("\n--- Change Login Password ---")
                a = 3
                while a > 0:
                    lp = input("\nEnter your current Login Password : ")
                    if hash_data(lp, acc[5]) == acc[3]:
                        new_salt = os.urandom(16).hex()
                        newpass = login_password()
                        cursor.execute("UPDATE accounts SET loginpass=?, loginpass_salt=? WHERE accid=?",
                                       (hash_data(newpass, new_salt), new_salt, acc[1]))
                        conn.commit()
                        print("\nLogin Password changed successfully.")
                        break
                    else:
                        a -= 1
                        print(f"\nIncorrect Login Password. {a} attempts left.")
                if a == 0:
                    print("Too many failed attempts.\n")

            elif opt == "8":
                print("\n--- Delete Account ---")
                a = 3
                while a > 0:
                    pin = input("\nEnter your MPIN : ")
                    if hash_data(pin, acc[6]) == acc[2]:
                        break
                    else:
                        a -= 1
                        print(f"Incorrect MPIN. {a} attempts left.\n")

                if a == 0:
                    print("Too many failed attempts.\n")
                    continue

                a = 3
                while a > 0:
                    lp = input("Enter your Login Password : ")
                    if hash_data(lp, acc[5]) == acc[3]:
                        while True:
                            confirm = input("\nAre you sure you want to delete this account? (y/n): ").lower()
                            if confirm in ("y", "yes"):
                                cursor.execute("DELETE FROM accounts WHERE accid=?", (acc[1],))
                                conn.commit()
                                print("Account", acc[0], "deleted.\n")
                                break
                            elif confirm in ("n", "no"):
                                print("Cancelled\n")
                                break
                            else:
                                print("Invalid input")
                        break
                    else:
                        a -= 1
                        print(f"Incorrect Login Password. {a} attempts left.\n")

                break

            elif opt == "9":
                print("\nThank you for using the Python Bank System. Logging out...\n")
                break

            else:
                print("Invalid option. Try again.\n")

    elif option == "4":
        print("\nThank you for using the Python Bank System. Goodbye!\n")
        break

    else:
        print("\nInvalid option. Try again.\n")
