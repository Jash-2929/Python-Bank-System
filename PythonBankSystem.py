import os
import random

filename = "accountdata.txt"

accounts=[]

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
                        print("MPIN created successfully.")
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

def read_accounts():
    accounts = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                parts = line.strip().split(",")
                if len(parts) == 5:
                    accounts.append({"name": parts[0], "accid": parts[1], "mpin": parts[2], "loginpass": parts[3], "balance": float(parts[4])})
    return accounts
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
        loginpass = ""

        name = input("Enter name for the new account: ")
        while not (name.replace(" ", "").isalpha() and not name.isspace()):
            print("Name can only contain alphabets and spaces, and cannot be only spaces.")
            name = input("Enter name for the new account: ")

        print("\n--- Create Login Password ---")
        print("You may enter alphabets, numbers or special characters.")
        print("The password must contain 8 to 12 characters only.\n")
        print("The password must contain an alphabet, a number and a special charater.")

        loginpass=login_password()
        print("Your password has been created.")

        print("\n--- Create MPIN ---")
        mpin=mpin_()

        accounts=read_accounts()

        while True:
            accid = "PBK" + str(random.randint(1000, 9999))
            if not any(acc["accid"] == accid for acc in accounts):
                break

        print("\nYour account ID is : ", accid)
        balance=input_float("Enter your starting balance : ")

        print("Congratulations! Your account has been created.\n")

        accounts.append({"name": name, "accid": accid, "mpin": mpin, "loginpass": loginpass, "balance": balance})

        with open(filename, "w") as file:
            for account in accounts:
                file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")

    elif option == "2":
        print("\n===== SHOW ALL ACCOUNTS =====\n")

        accounts=read_accounts()

        if not accounts:
            print("No accounts found.\n")
        else:
            print("--- List of All Accounts ---\n")
            for i in range(0,len(accounts)):
                print(f"{i+1}. {accounts[i]['name']} - {accounts[i]['accid']}")
            print()

    elif option == "3":
        print("\n===== LOGIN =====\n")

        accounts = read_accounts()

        if not len(accounts):
            print("No accounts to login.\n")
        else:
            for i,acc in enumerate(accounts,1):
                print(f"{i}. {acc['name']} - {acc['accid']}")
            choice=input_int("\nChoose sr. number of account to login : ")

            if not (1 <= choice <= len(accounts)):
                print("Invalid choice\n")
            else:
                choice-=1
                attempts=3
                while attempts>0:
                    loginpass = input("Enter Login Password : ")
                    if not loginpass == accounts[choice]['loginpass']:
                        attempts -= 1
                        print(f"\nIncorrect Login Password. {attempts} attempts left.\n")
                    else:
                        print(f"\nWelcome {accounts[choice]['name']}!\n")

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

                            if accopt == "1":
                                print("\n--- Account Details ---")
                                print(f"Name       : {accounts[choice]['name']}")
                                print(f"Account ID : {accounts[choice]['accid']}")
                                print(f"Balance    : {accounts[choice]['balance']}\n")

                            elif accopt == "2":
                                print("\n--- Withdraw ---")
                                amount = input_float("Enter amount to withdraw : ")
                                attempts=3
                                while attempts>0:
                                    pin = input("Enter your MPIN : ")
                                    if pin == accounts[choice]['mpin']:
                                        if amount <= accounts[choice]['balance'] and amount>0:
                                            accounts[choice]['balance'] -= amount
                                            with open(filename, "w") as file:
                                                for account in accounts:
                                                    file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                            print("Withdrawal successful. Your new balance is : ",accounts[choice]['balance'])
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
                                    if pin == accounts[choice]['mpin']:
                                        if amount > 0:
                                            accounts[choice]['balance'] += amount
                                            with open(filename, "w") as file:
                                                for account in accounts:
                                                    file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                            print("Deposit successful. Your new balance is : ",accounts[choice]['balance'])
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
                                    if pin == accounts[choice]['mpin']:
                                        newmpin=mpin_()
                                        accounts[choice]['mpin'] = newmpin
                                        with open(filename, "w") as file:
                                            for account in accounts:
                                                file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                        print("\nMPIN changed successfully.")
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
                                    if login == accounts[choice]['loginpass']:
                                        print("\nYou may enter alphabets, numbers or special characters.")
                                        print("The password must contain 8 to 12 characters only.")
                                        print("The password must contain an alphabet, a number and a special character.")
                                        loginpass=login_password()
                                        accounts[choice]['loginpass'] = loginpass
                                        with open(filename, "w") as file:
                                            for account in accounts:
                                                file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                        print("\nLogin Password changed successfully.")
                                        break
                                    else:
                                        attempts-=1
                                        print(f"\nIncorrect Login Password. {attempts} attempts left.")
                                if attempts==0:
                                    print("Too many failedattempts. Returning to account menu.")
                                    continue

                            elif accopt == "6":
                                print("\n--- Delete Account ---")
                                attempts=3
                                while attempts>0:
                                    pin = input("\nEnter your MPIN : ")
                                    if pin == accounts[choice]['mpin']:
                                        confirm = input("\nAre you sure you want to delete this account? (y/n): ").lower()
                                        if confirm in ("y", "yes"):
                                            displayname = accounts[choice]['name']
                                            del accounts[choice]
                                            with open(filename, "w") as file:
                                                for account in accounts:
                                                    file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                                print("Account", displayname, "deleted.\n")
                                            deleted=True
                                            break
                                        elif confirm in ("n", "no"):
                                            print("Cancelled")
                                        else:
                                            print("Invalid input")
                                    else:
                                        attempts-=1
                                        print(f"Incorrect MPIN. {attempts} attempts left.\n")
                                        print("Account not deleted.\n")
                                if deleted:
                                    break
                                if attempts == 0:
                                    print("Too many failed attempts. Returning to account menu...")
                                else:
                                    break

                            elif accopt == "7":
                                print("\nThank you for using the Python Bank System. Logging out...\n")
                                break

                            else:
                                print("Invalid option. Try again.\n")
                        break
                if attempts == 0:
                    print("Too many failed attempts. Returning to main menu...\n")
                    continue

    elif option == "4":
        print("\nThank you for using the Python Bank System. Goodbye!\n")
        break

    else:
        print("\nInvalid option. Try again.\n")
