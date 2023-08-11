import hashlib
import getpass
from cryptography.fernet import Fernet

USERS_FILE = "users.txt"
WALLETS_FILE = "wallets.txt"

# Helper function to read user data from the file
def read_users_data():
    try:
        with open(USERS_FILE, "r") as file:
            data = file.read()
            if data:
                users_data = {}
                for line in data.split("\n"):
                    if line:
                        username, email, password_hash = line.split(",")
                        users_data[username] = {
                            "email": email,
                            "password_hash": password_hash
                        }
                return users_data
    except FileNotFoundError:
        pass
    return {}

# Helper function to save user data to the file
def save_users_data(users_data):
    with open(USERS_FILE, "w") as file:
        for username, user_data in users_data.items():
            file.write(f"{username},{user_data['email']},{user_data['password_hash']}\n")

# Helper function to read wallet balances from the file
def read_wallets_data():
    try:
        with open(WALLETS_FILE, "r") as file:
            data = file.read()
            if data:
                wallets_data = {}
                for line in data.split("\n"):
                    if line:
                        username, balance = line.split(",")
                        wallets_data[username] = {'balance': float(balance)}
                return wallets_data
    except FileNotFoundError:
        pass
    return {}

# Helper function to save wallet balances to the file
def save_wallets_data(wallets_data):
    with open(WALLETS_FILE, "w") as file:
        for username, wallet_data in wallets_data.items():
            file.write(f"{username},{wallet_data['balance']}\n")

# Load initial user data and wallet balances from the files
users = read_users_data()
wallets = read_wallets_data()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register():
    print("Welcome! Let's create your e-wallet.")
    username = input("Enter your username: ")
    if username in users:
        print("Username already exists. Please choose another username.")
        return

    email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    # Save user details to the memory and file
    users[username] = {'email': email, 'password_hash': hashed_password}
    save_users_data(users)

    # Set the initial balance to 0.0 and save it to the file
    initial_balance = 0.0  # Default initial balance is set to 0
    wallets[username] = {'balance': initial_balance}
    save_wallets_data(wallets)

    print("Registration successful!")

def login():
    print("Welcome back! Please login to access your e-wallet.")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")  # Hide password input

    # Check if the user exists and the password is correct
    if username in users and users[username]['password_hash'] == hash_password(password):
        print(f"Welcome, {username}!")

        while True:
            print("\nSelect an option:")
            print("1. Check Wallet Balance")
            print("2. Transfer Funds")
            print("3. Logout")

            choice = input("> ")

            if choice == '1':
                wallet(username)
            elif choice == '2':
                transfer_funds(username)
            elif choice == '3':
                print("Logged out.")
                return
            else:
                print("Invalid choice. Please try again.")

    else:
        print("Invalid credentials. Please try again or register.")

def wallet(username):
    if username in wallets:
        balance = wallets[username]['balance']
        print(f"Wallet balance for {username}: {balance}")
    else:
        print("User not found. Please log in or register.")

def transfer_funds(username):
    if username not in wallets:
        print("User not found. Please log in or register.")
        return

    recipient = input("Enter the recipient's username: ")
    if recipient not in wallets:
        print("Recipient not found.")
        return

    amount = float(input("Enter the amount to transfer: "))
    if amount <= 0:
        print("Invalid amount. Please enter a positive number.")
        return

    if wallets[username]['balance'] >= amount:
        wallets[username]['balance'] -= amount
        wallets[recipient]['balance'] += amount
        save_wallets_data(wallets)  # Save updated wallet balances to the file
        print(f"Successfully transferred {amount} to {recipient}.")
    else:
        print("Insufficient balance.")

def main():
    print("Welcome to the e-wallet CLI!")

    # Loop to keep the program running until the user chooses to exit
    while True:
        print("\nSelect an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("> ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Thank you for using the e-wallet CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
