 #🎴kenny
#06/08/2024
import base64
from cryptography.fernet import Fernet
from pymongo import MongoClient
from getpass import getpass
from datetime import datetime
import time
import threading

# MongoDB Atlas connection details
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/test"  # Replace with your MongoDB Atlas URI

# Chat room settings
MAX_CLIENTS = 2  # Maximum number of clients allowed in a chat room

# Function to get user credentials
def get_credentials():
    username = input("Enter your codename: ")
    passcode = input("Enter the chatroom passcode: ")
    return username, passcode

# Function to connect to MongoDB Atlas
def connect_to_mongodb():
    client = MongoClient(MONGO_URI)
    return client

# Function to generate a new Fernet key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a message
def encrypt_message(key, message):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

# Function to decrypt a message
def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()

# Function to join the chat room
def join_chat_room(collection, username, passcode):
    chat_room = f"CHAT_{passcode}"
    room_info = collection.find_one({"_id": chat_room})
    if room_info is None:
        room_key = generate_key()
        collection.insert_one({
            "_id": chat_room,
            "users": [username],
            "messages": [],
            "room_key": base64.urlsafe_b64encode(room_key).decode(),
            "passcode": passcode
        })
        print("🏳️ Created a new private chat room. Waiting for other users to join...")
        return room_key
    elif len(room_info["users"]) < MAX_CLIENTS and username not in room_info["users"]:
        collection.update_one({"_id": chat_room}, {"$push": {"users": username}})
        print(f"Joined the private chat room with {', '.join(room_info['users'][:-1])}")
        return base64.urlsafe_b64decode(room_info["room_key"].encode())
    else:
        print("Private chat room is full or you're already in it.")
        return None

# Function to send a message
def send_message(collection, username, message, chat_room, key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    encrypted_message = encrypt_message(key, message)
    message_data = {
        "timestamp": timestamp,
        "username": username,
        "encrypted_message": encrypted_message
    }
    collection.update_one({"_id": chat_room}, {"$push": {"messages": message_data}})

# Function to retrieve and display new messages
def get_new_messages(collection, chat_room, last_index, key, username):
    room_info = collection.find_one({"_id": chat_room})
    messages = room_info["messages"][last_index:]
    for msg in messages:
        if msg["username"] != username:
            decrypted_message = decrypt_message(key, msg['encrypted_message'])
            print(f"[{msg['timestamp']}] {msg['username']}: {decrypted_message}")
    return len(room_info["messages"])

# Function to continuously check for new messages
def message_listener(collection, username, chat_room, key):
    last_index = 0
    while True:
        last_index = get_new_messages(collection, chat_room, last_index, key, username)
        time.sleep(1)  # Check for new messages every second

# Function to leave the chat room and cleanup
def leave_chat_room(collection, username, chat_room):
    collection.update_one({"_id": chat_room}, {"$pull": {"users": username}})
    room_info = collection.find_one({"_id": chat_room})
    if not room_info["users"]:
        collection.delete_one({"_id": chat_room})
        print("🏴 Chat room closed and messages deleted.")
    else:
        print(f"Left the chat room.")

# Main function
def main():
    username, passcode = get_credentials()
    try:
        client = connect_to_mongodb()
        db = client['chat_database']
        collection = db['chat_collection']
        print(f"Connected to the chat as {username}")

        chat_room = f"CHAT_{passcode}"
        room_key = join_chat_room(collection, username, passcode)
        if room_key is None:
            return

        listener_thread = threading.Thread(target=message_listener, args=(collection, username, chat_room, room_key))
        listener_thread.daemon = True
        listener_thread.start()

        while True:
            message = input()
            if message.lower() == '/quit':
                break
            send_message(collection, username, message, chat_room, room_key)

        leave_chat_room(collection, username, chat_room)
        client.close()

    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    main()