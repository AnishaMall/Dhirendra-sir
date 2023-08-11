import subprocess

def greet_and_choose_interface():
    print("Welcome to your personal wallet!")
    interface_choice = input("What interface do you choose? Enter 1 for CLI or 2 for GUI: ")

    if interface_choice == '1':
        try:
            subprocess.run(['python', 'wallet_cli.py'], check=True)
        except FileNotFoundError:
            print("Error: wallet_cli.py not found.")
    elif interface_choice == '2':
        try:
            subprocess.run(['python', 'wallet_gui.py'], check=True)
        except FileNotFoundError:
            print("Error: wallet_gui.py not found.")
    else:
        print("Invalid choice. Please enter either 1 or 2.")

if __name__ == "__main__":
    greet_and_choose_interface()
