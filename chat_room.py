from secure_messenger import SecureMessenger

class ChatRoom:
    def __init__(self, encryption_key):
        self.messenger = SecureMessenger(encryption_key)
        self.users = {}

    def register_user(self, username):
        if username in self.users:
            raise ValueError(f"Username '{username}' already exists.")
        self.users[username] = []

    def send_message(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            raise ValueError("Invalid sender or receiver.")
        encrypted_message = self.messenger.encrypt_message(message)
        self.users[receiver].append((sender, encrypted_message))

    def retrieve_messages(self, user_id):
        if user_id not in self.users:
            raise ValueError(f"User '{user_id}' does not exist.")
        messages = self.users[user_id]
        self.users[user_id] = []  # Clear retrieved messages
        decrypted_messages = [f"{sender}: {self.messenger.decrypt_message(encrypted_message)}"
                              for sender, encrypted_message in messages]
        return decrypted_messages
