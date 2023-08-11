import tkinter as tk
from tkinter import messagebox
from chat_room import ChatRoom

class ChatGUI:
    def __init__(self):
        self.encryption_key = b'gH7cGjTBEzyV-NY_HPLypTQwfto--eFjQ_2Dr5a4QK8='  # Set your own encryption key
        self.chat_room = ChatRoom(self.encryption_key)

        self.window = tk.Tk()
        self.window.title("Secure Messaging - GUI")

        self.sender_label = tk.Label(self.window, text="Sender:")
        self.sender_label.pack()
        self.sender_entry = tk.Entry(self.window)
        self.sender_entry.pack()

        self.receiver_label = tk.Label(self.window, text="Receiver:")
        self.receiver_label.pack()
        self.receiver_entry = tk.Entry(self.window)
        self.receiver_entry.pack()

        self.message_label = tk.Label(self.window, text="Message:")
        self.message_label.pack()
        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack()

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()

        self.register_button = tk.Button(self.window, text="Register User", command=self.register_user)
        self.register_button.pack()

        self.view_messages_button = tk.Button(self.window, text="View Messages", command=self.view_messages)
        self.view_messages_button.pack()

    def send_message(self):
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        message = self.message_entry.get()

        try:
            self.chat_room.send_message(sender, receiver, message)
            messagebox.showinfo("Message Sent", "Message sent successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        self.sender_entry.delete(0, tk.END)
        self.receiver_entry.delete(0, tk.END)
        self.message_entry.delete(0, tk.END)

    def register_user(self):
        username = self.sender_entry.get()
        try:
            self.chat_room.register_user(username)
            messagebox.showinfo("User Registered", f"User '{username}' registered successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        self.sender_entry.delete(0, tk.END)

    def view_messages(self):
        username = self.sender_entry.get()
        try:
            messages = self.chat_room.retrieve_messages(username)
            if messages:
                messagebox.showinfo("Messages", f"Messages for user '{username}':\n\n{messages}")
            else:
                messagebox.showinfo("No Messages", f"No messages found for user '{username}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        self.sender_entry.delete(0, tk.END)

    def run_gui(self):
        self.window.mainloop()

