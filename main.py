import cui
import gui

def main():
    while True:
        print("\nSecure Messaging Application")
        print("1. Command-line Interface (CUI)")
        print("2. Graphical User Interface (GUI)")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            cui.run_cui()
        elif choice == '2':
            chat_gui = gui.ChatGUI()
            chat_gui.run_gui()
        elif choice == '3':
            exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
