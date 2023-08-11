import hashlib
import tkinter as tk
from tkinter import messagebox

# In-memory storage for user data and wallet balances
users_data = {}
wallets_data = {}

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Function to save user data to file
def save_users_data():
    with open("users.txt", "w") as file:
        for username, user_data in users_data.items():
            file.write(f"{username},{user_data['email']},{user_data['password_hash']}\n")

# Function to save wallet balances to file
def save_wallets_data():
    with open("wallets.txt", "w") as file:
        for username, wallet_data in wallets_data.items():
            file.write(f"{username},{wallet_data['balance']}\n")

# Function to load user data from file
def load_users_data():
    try:
        with open("users.txt", "r") as file:
            for line in file:
                username, email, password_hash = line.strip().split(',')
                users_data[username] = {'email': email, 'password_hash': password_hash}
    except FileNotFoundError:
        pass

# Function to load wallet balances from file
def load_wallets_data():
    try:
        with open("wallets.txt", "r") as file:
            for line in file:
                username, balance = line.strip().split(',')
                wallets_data[username] = {'balance': float(balance)}
    except FileNotFoundError:
        pass

# Function to save data to files
def save_data():
    save_users_data()
    save_wallets_data()

# GUI functions for individual pages
def show_register_page():
    main_frame.grid_forget()  # Hide main page frame
    register_frame.grid(row=0, column=0, padx=20, pady=20)

    # Define the entry widgets as global variables
    global username_entry_reg, email_entry, password_entry
    username_entry_reg = tk.Entry(register_frame)
    tk.Label(register_frame, text="Confirm Username:").pack(pady=5)
    username_entry_reg.pack(pady=5)
    email_entry = tk.Entry(register_frame)
    tk.Label(register_frame, text="Confirm Email:").pack(pady=5)
    email_entry.pack(pady=5)
    password_entry = tk.Entry(register_frame, show="*")
    tk.Label(register_frame, text="Confirm Password:").pack(pady=5)
    password_entry.pack(pady=5)

def register():
    global username_entry_reg, email_entry, password_entry

    username = username_entry_reg.get()
    email = email_entry.get()
    password = password_entry.get()
    hashed_password = hash_password(password)

    if username == "" or email == "" or password == "":
        messagebox.showerror("Error", "Please fill in all the required fields.")
    elif username in users_data:
        messagebox.showerror("Error", "Username already exists. Please choose another username.")
    else:
        users_data[username] = {'email': email, 'password_hash': hashed_password}
        save_data()

        # Set the initial balance to 0.0 and save it to the memory
        initial_balance = 0.0  # Default initial balance is set to 0
        wallets_data[username] = {'balance': initial_balance}
        save_wallets_data()

        show_message_box("Registration", "Registration successful!")
        show_main_page(register_frame)

# Function to create the GUI
def create_gui():
    global root, main_frame, register_frame, login_frame
    global username_entry_reg, email_entry, password_entry
    global username_entry_login, password_entry_login

    root = tk.Tk()
    root.title("E-Wallet Application")

    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, padx=20, pady=20)

    tk.Label(main_frame, text="Welcome to E-Wallet", font=("Helvetica", 20)).pack(pady=10)

    options = [
        ("Register", show_register_page),
        ("Login", show_login_page),
        ("Exit", exit_application)
    ]

    for text, command in options:
        tk.Radiobutton(main_frame, text=text, font=("Helvetica", 12), value=command, indicatoron=0, width=20,
                       command=command).pack(pady=5)

    register_frame = tk.Frame(root)
    login_frame = tk.Frame(root)


def show_login_page():
    main_frame.grid_forget()  # Hide main page frame
    login_frame.grid(row=0, column=0, padx=20, pady=20)

def login():
    global username_entry_login, password_entry_login

    username = username_entry_login.get()
    password = password_entry_login.get()
    hashed_password = hash_password(password)

    if username in users_data and users_data[username]['password_hash'] == hashed_password:
        show_message_box("Login", f"Welcome, {username}!")
        show_wallet_page(username)
        save_data()  # Save data after successful login
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again or register.")

def show_wallet_page(username):
    login_frame.grid_forget()
    wallet_frame = tk.Frame(root)
    wallet_frame.grid(row=0, column=0, padx=20, pady=20)

    tk.Label(wallet_frame, text=f"Welcome, {username}!", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(wallet_frame, text="Check Balance", font=("Helvetica", 12), command=lambda: check_balance(username)).pack(pady=5)
    tk.Button(wallet_frame, text="Transfer Funds", font=("Helvetica", 12), command=lambda: show_transfer_page(username)).pack(pady=5)
    tk.Button(wallet_frame, text="Logout", font=("Helvetica", 12), command=lambda: show_main_page(wallet_frame)).pack(pady=5)

def check_balance(username):
    balance = wallets_data[username]['balance']
    show_message_box("Wallet Balance", f"Wallet balance for {username}: {balance}")

def show_transfer_page(sender):
    transfer_window = tk.Toplevel(root)  # Create a new window for the transfer
    transfer_window.title("Transfer Funds")
    transfer_window.geometry("300x200")

    tk.Label(transfer_window, text="Transfer Funds", font=("Helvetica", 16)).pack(pady=10)

    recipient_label = tk.Label(transfer_window, text="Recipient Username:")
    recipient_label.pack(pady=5)
    recipient_entry = tk.Entry(transfer_window)
    recipient_entry.pack(pady=5)

    amount_label = tk.Label(transfer_window, text="Amount:")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(transfer_window)
    amount_entry.pack(pady=5)

    tk.Button(transfer_window, text="Transfer", font=("Helvetica", 12),
              command=lambda: transfer_funds(sender, recipient_entry.get(), float(amount_entry.get()))).pack(pady=5)

def transfer_funds(sender, recipient, amount):
    if sender not in wallets_data or recipient not in wallets_data:
        messagebox.showerror("Error", "Invalid sender or recipient.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
        return

    if wallets_data[sender]['balance'] >= amount:
        wallets_data[sender]['balance'] -= amount
        wallets_data[recipient]['balance'] += amount
        save_data()  # Save data after successful transfer
        show_message_box("Transfer", f"Successfully transferred {amount} to {recipient}.")
    else:
        messagebox.showerror("Error", "Insufficient balance.")


def exit_application():
    root.destroy()

# Function to create the GUI
def create_gui():
    global root, main_frame, register_frame, login_frame
    global username_entry_login, password_entry_login

    # Load user data and wallet balances from files
    load_users_data()
    load_wallets_data()

    root = tk.Tk()
    root.title("E-Wallet Application")

    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, padx=20, pady=20)

    tk.Label(main_frame, text="Welcome to E-Wallet", font=("Helvetica", 20)).pack(pady=10)

    options = [
        ("Register", show_register_page),
        ("Login", show_login_page),
        ("Exit", exit_application)
    ]

    for text, command in options:
        tk.Radiobutton(main_frame, text=text, font=("Helvetica", 12), value=command, indicatoron=0, width=20,
                       command=command).pack(pady=5)

    register_frame = tk.Frame(root)
    login_frame = tk.Frame(root)

    tk.Label(register_frame, text="Register Page", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(register_frame, text="Username:").pack(pady=5)
    username_entry_reg = tk.Entry(register_frame)
    username_entry_reg.pack(pady=5)
    tk.Label(register_frame, text="Email:").pack(pady=5)
    email_entry = tk.Entry(register_frame)
    email_entry.pack(pady=5)
    tk.Label(register_frame, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_frame, show="*")
    password_entry.pack(pady=5)
    tk.Button(register_frame, text="Register", font=("Helvetica", 12), command=register).pack(pady=5)
    tk.Button(register_frame, text="Back", font=("Helvetica", 12), command=lambda: show_main_page(register_frame)).pack(pady=5)

    tk.Label(login_frame, text="Login Page", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(login_frame, text="Username:").pack(pady=5)
    username_entry_login = tk.Entry(login_frame)
    username_entry_login.pack(pady=5)
    tk.Label(login_frame, text="Password:").pack(pady=5)
    password_entry_login = tk.Entry(login_frame, show="*")
    password_entry_login.pack(pady=5)
    tk.Button(login_frame, text="Login", font=("Helvetica", 12), command=login).pack(pady=5)
    tk.Button(login_frame, text="Back", font=("Helvetica", 12), command=lambda: show_main_page(login_frame)).pack(pady=5)

    root.mainloop()

def show_main_page(frame):
    frame.grid_forget()
    main_frame.grid(row=0, column=0, padx=20, pady=20)

def show_message_box(title, message):
    messagebox.showinfo(title, message)

if __name__ == "__main__":
    # Load user data and wallet balances from files
    load_users_data()
    load_wallets_data()

    create_gui()