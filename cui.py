from chat_room import ChatRoom

def run_cui():
    encryption_key = b'gH7cGjTBEzyV-NY_HPLypTQwfto--eFjQ_2Dr5a4QK8='  # Set your own encryption key
    chat_room = ChatRoom(encryption_key)

    while True:
        print("\nSecure Messaging Application - CUI")
        print("1. Register User")
        print("2. Send Message")
        print("3. Retrieve Messages")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Enter the username: ")
            try:
                chat_room.register_user(username)
                print(f"User '{username}' registered successfully!")
            except ValueError as e:
                print(f"Error: {str(e)}")
        elif choice == '2':
            sender = input("Enter the sender: ")
            receiver = input("Enter the receiver: ")
            message = input("Enter the message: ")
            try:
                chat_room.send_message(sender, receiver, message)
                print("Message sent successfully!")
            except ValueError as e:
                print(f"Error: {str(e)}")
        elif choice == '3':
            user_id = input("Enter the user ID to retrieve messages: ")
            try:
                messages = chat_room.retrieve_messages(user_id)
                if messages:
                    print(f"Messages for user '{user_id}':")
                    for message in messages:
                        print(message)
                else:
                    print(f"No messages found for user '{user_id}'.")
            except ValueError as e:
                print(f"Error: {str(e)}")
        elif choice == '4':
            exit()
        else:
            print("Invalid choice. Please try again.")

