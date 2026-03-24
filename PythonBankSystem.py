import os
import random

filename = "accountdata.txt"

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
        alpha = 0
        num = 0
        char = 0        
        p = 0
        q = 0
        r = 0
        s = 0
        u = 0
        name1 = 0
        loginpass = ""
        while u == 0:
            name = input("Enter name for the new account : ")
            for i in name:
                if i.isalpha():
                    name1 = name1
                elif i.isnum():
                    name1 += 1
                else:
                    name1 += 1
            if name1 > 0:
                print("Name can only have alphabets.")
            else:
                u = 1
                
        print("\n--- Create Login Password ---")
        print("You may enter alphabets, numbers or special characters.")
        print("The password must contain 8 to 12 characters only.\n")
        while q == 0:
            while r == 0:
                password = input("Enter your Login Password : ")
                if 8 <= len(password) <= 12:
                    q = 1
                    for i in password:
                        if i.isalpha():
                            alpha += 1
                        elif i.isdigit():
                            num += 1
                        else:
                            char += 1
                    if alpha > 0:
                        if num > 0:
                            if char > 0:
                                print("The strength of your password is Strong.")
                                r = 1
                                loginpass = password
                                while s == 0:
                                    con = input("Enter your Login Password again to confirm : ")
                                    if con == loginpass:
                                        print("Your password is created")
                                        s = 1
                                    else:
                                        print("The password does not match")
                            else:
                                print("The strength of your password is Medium")
                        elif num == 0:
                            if char > 0:
                                print("The strength of your password is Medium")
                            else:
                                print("The strength of your password is Weak")
                    elif alpha == 0:
                        if num > 0:
                            if char > 0:
                                print("The strength of your password is Medium")
                            else:
                                print("The strength of your password is Weak")
                        elif num == 0:
                            print("The strength of your password is Weak")
                else:
                    print("Please enter a password consisting of 8 to 12 characters.")

        print("\n--- Create MPIN ---")
        print("Following are the choices for length of the MPIN.")
        print("1. 4-Digit MPIN")
        print("2. 6-Digit MPIN\n")
        while p == 0:
            mpinchoice = input("Choose from the given options : ")
            if mpinchoice == "1":
                mpin = input("Enter your 4-Digit MPIN : ")
                if len(mpin) == 4 and mpin.isdigit():
                    print("Your MPIN has been created!")
                    p = 1
                else:
                    print("Please enter a valid MPIN.")
            elif mpinchoice == "2":
                mpin = input("Enter your 6-Digit MPIN : ")
                if len(mpin) == 6 and mpin.isdigit():
                    print("Your MPIN has been created!")
                    p = 1
                else:
                    print("Please enter a valid MPIN.")
            else:
                print("Please select from the given options only.")

        accounts = []
        if os.path.exists(filename):
            with open(filename, "r") as file:
                for line in file.readlines():
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        accounts.append({"name": parts[0], "accid": parts[1], "mpin": parts[2], "loginpass": parts[3], "balance": parts[4]})
        while True:
            accid = "PBK" + str(random.randint(1000, 9999))
            if not any(acc["accid"] == accid for acc in accounts):
                break
        
        print("\nYour account ID is : ", accid)
        balance = float(input("Enter your starting balance : "))
        print("Congratulations! Your account has been created.\n")
        accounts = []
        if os.path.exists(filename):
            with open(filename, "r") as file:
                for line in file.readlines():
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        accounts.append({"name": parts[0], "accid": parts[1], "mpin": parts[2], "loginpass": parts[3], "balance": parts[4]})
        accounts.append({"name": name, "accid": accid, "mpin": mpin, "loginpass": loginpass, "balance": balance})

        with open(filename, "w") as file:
            for account in accounts:
                file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")

    elif option == "2":
        print("\n===== SHOW ALL ACCOUNTS =====\n")
        accounts = []
        if os.path.exists(filename):
            with open(filename, "r") as file:
                for line in file.readlines():
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        accounts.append({"name": parts[0], "accid": parts[1], "mpin": parts[2], "loginpass": parts[3], "balance": float(parts[4])})
        if not accounts:
            print("No accounts found.\n")
        else:
            print("--- List of All Accounts ---\n")
            i = 0
            while i < len(accounts):
                print(f"{i+1}. {accounts[i]['name']} - {accounts[i]['accid']}")
                i += 1
            print()

    elif option == "3":
        print("\n===== LOGIN =====\n")
        accounts = []
        if os.path.exists(filename):
            with open(filename, "r") as file:
                for line in file.readlines():
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        accounts.append({"name": parts[0], "accid": parts[1], "mpin": parts[2], "loginpass": parts[3], "balance": float(parts[4])})
        if not accounts:
            print("No accounts to login.\n")
        else:
            i = 0
            while i < len(accounts):
                print(f"{i+1}. {accounts[i]['name']} - {accounts[i]['accid']}")
                i += 1
            choice = int(input("\nChoose account number to login : "))

            if choice < 0 or choice > len(accounts):
                print("Invalid choice\n")
            else:
                choice -= 1
                loginpass = input("Enter Login Password : ")
                if loginpass == accounts[choice]['loginpass']:
                    print(f"\nWelcome {accounts[choice]['name']}!\n")

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
                            amount = float(input("Enter amount to withdraw : "))
                            pin = input("Enter your MPIN : ")
                            if pin == accounts[choice]['mpin']:
                                if amount <= accounts[choice]['balance']:
                                    accounts[choice]['balance'] -= amount
                                    with open(filename, "w") as file:
                                        for account in accounts:
                                            file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                    print("Withdrawal successful. Your new balance is : ", accounts[choice]['balance'])
                                else:
                                    print("Insufficient balance.")
                            else:
                                print("Incorrect MPIN")

                        elif accopt == "3":
                            print("\n--- Deposit ---")
                            amount = float(input("Enter amount to deposit : "))
                            pin = input("Enter your MPIN : ")
                            if pin == accounts[choice]['mpin']:
                                if amount > 0:
                                    accounts[choice]['balance'] += amount
                                    with open(filename, "w") as file:
                                        for account in accounts:
                                            file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                    print("Deposit successful. Your new balance is : ", accounts[choice]['balance'])
                                else:
                                    print("Please enter an amount greater than 0")
                            else:
                                print("Incorrect MPIN")

                        elif accopt == "4":
                            print("\n--- Change MPIN ---")
                            pin = input("Enter your current MPIN : ")
                            if pin == accounts[choice]['mpin']:
                                t = 0
                                print("\nFollowing are the choices for length of the MPIN.")
                                print("1. 4-Digit MPIN")
                                print("2. 6-Digit MPIN")
                                while t == 0:
                                    mpinchoice = input("\nChoose from the given options : ")
                                    if mpinchoice == "1":
                                        newmpin = input("\nEnter your new 4-Digit MPIN : ")
                                        if len(mpin) == 4 and mpin.isdigit():
                                            t = 1
                                        else:
                                            print("\nPlease enter a valid MPIN.")
                                    elif mpinchoice == "2":
                                        newmpin = input("\nEnter your new 6-Digit MPIN : ")
                                        if len(newmpin) == 6 and newmpin.isdigit():
                                            t = 1
                                        else:
                                            print("\nPlease enter a valid MPIN.")
                                    else:
                                        print("\nPlease select from the given options only.")

                                accounts[choice]['mpin'] = newmpin
                                with open(filename, "w") as file:
                                    for account in accounts:
                                        file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                print("\nMPIN changed successfully.")
                            else:
                                print("\nIncorrect MPIN")
                            
                        elif accopt == "5":
                            print("\n--- Change Login Password ---")
                            login = input("\nEnter your current Login Password : ")
                            if login == accounts[choice]['loginpass']:
                                alpha = 0
                                num = 0
                                char = 0        
                                p = 0
                                q = 0
                                r = 0
                                s = 0
                                newlpass = ""
                                print("\nYou may enter alphabets, numbers or special characters.")
                                print("The password must contain 8 to 12 characters only.")
                                while q == 0:
                                    while r == 0:
                                        newlpass = input("\nEnter your new Login Password : ")
                                        if 8 <= len(newlpass) <= 12:
                                            q = 1
                                            for i in newlpass:
                                                if i.isalpha():
                                                    alpha += 1
                                                elif i.isdigit():
                                                    num += 1
                                                else:
                                                    char += 1
                                            if alpha > 0:
                                                if num > 0:
                                                    if char > 0:
                                                        print("The strength of your password is Strong.")
                                                        r = 1
                                                        loginpass = newlpass
                                                        while s == 0:
                                                            con = input("\nEnter your Login Password again to confirm : ")
                                                            if con == loginpass:
                                                                s = 1
                                                                with open(filename, "w") as file:
                                                                    for account in accounts:
                                                                        file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                                                print("\nLogin Password changed successfully.")
                                                            else:
                                                                print("\nThe password does not match")
                                                    else:
                                                        print("\nThe strength of your password is Medium")
                                                elif num == 0:
                                                    if char > 0:
                                                        print("\nThe strength of your password is Medium")
                                                    else:
                                                        print("\nThe strength of your password is Weak")
                                            elif alpha == 0:
                                                if num > 0:
                                                    if char > 0:
                                                        print("\nThe strength of your password is Medium")
                                                    else:
                                                        print("\nThe strength of your password is Weak")
                                                elif num == 0:
                                                    print("\nThe strength of your password is Weak")
                                        else:
                                            print("\nPlease enter a password consisting of 8 to 12 characters.")
                            else:
                                print("\nIncorrect Login Password")
                        
                        elif accopt == "6":
                            print("\n--- Delete Account ---")
                            pin = input("\nEnter your MPIN : ")
                            if pin == accounts[choice]['mpin']:
                                confirm = input("\nAre you sure you want to delete this account? (y/n) : ")
                                if confirm.lower() in ("y", "yes"):
                                    displayname = accounts[choice]['name']
                                    del accounts[choice]
                                    with open(filename, "w") as file:
                                        for account in accounts:
                                            file.write(f"{account['name']},{account['accid']},{account['mpin']},{account['loginpass']},{account['balance']}\n")
                                        print("Account", displayname, "deleted.\n")
                                        break
                                else:
                                    print("Account not deleted.\n")
                            else:
                                print("Incorrect MPIN\n")
                                print("Account not deleted.\n")

                        elif accopt == "7":
                            print("\nThank you for using the Python Bank System. Logging out...\n")
                            break

                        else:
                            print("Invalid option. Try again.\n")
                else:
                    print("\nIncorrect MPIN\n")

    elif option == "4":
        print("\nThank you for using the Python Bank System. Goodbye!\n")
        break

    else:
        print("\nInvalid option. Try again.\n")
