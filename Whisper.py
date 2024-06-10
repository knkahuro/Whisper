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
MONGO_URI = #enter your MongoDB Atlas URI here

# Chat room settings
CHAT_ROOM = "PRIVATE CHAT"
MAX_CLIENTS = 2  # default is two but can add or deduct if you want

# Function to get user credentials
def get_credentials():
    username = input("Enter codename: ")
    passcode = getpass("Enter chatroom passcode: ")
    return username, passcode

# Function to connect to MongoDB Atlas
def connect_to_mongodb():
    client = MongoClient(MONGO_URI)
    return client

# Function to generate a new Fernet key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt message 
def encrypt_message(key, message):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode() 

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()

# Function to join chat room
def join_chat_room(collection, username, chat_room, passcode):
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
        print("🏳️Created private chat room. Waiting for another user to join...")
        return room_key
    elif room_info["passcode"] != passcode:
        print("Incorrect passcode. Access denied.")
        return None
    elif len(room_info["users"]) < MAX_CLIENTS and username not in room_info["users"]:
        collection.update_one({"_id": chat_room}, {"$push": {"users": username}})
        print(f"Joined the private chat room with {room_info['users'][0]}")
        return base64.urlsafe_b64decode(room_info["room_key"].encode())
    else:
        print("Private chat room is full or you're already in it.")
        return None

# Function to send a message
def send_message(collection, username, message, key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    encrypted_message = encrypt_message(key, message)
    message_data = {
        "timestamp": timestamp,
        "username": username,
        "encrypted_message": encrypted_message
    }
    collection.update_one({"_id": CHAT_ROOM}, {"$push": {"messages": message_data}})
    print(f"Sent at {timestamp}")

# Function to retrieve and display new messages
def get_new_messages(collection, last_index, key):
    room_info = collection.find_one({"_id": CHAT_ROOM})
    messages = room_info["messages"][last_index:]
    for msg in messages:
        decrypted_message = decrypt_message(key, msg['encrypted_message'])
        print(f"[{msg['timestamp']}] {msg['username']}: {decrypted_message}")
    return len(room_info["messages"])

# Function to continuously check for new messages
def message_listener(collection, username, key):
    last_index = 0
    while True:
        last_index = get_new_messages(collection, last_index, key)
        time.sleep(1)  # checks every one second to update

# Function to leave the chat room and cleanup
def leave_chat_room(collection, username):
    collection.update_one({"_id": CHAT_ROOM}, {"$pull": {"users": username}})
    room_info = collection.find_one({"_id": CHAT_ROOM})
    if not room_info["users"]:
        collection.delete_one({"_id": CHAT_ROOM})
        print("🏴Chat room closed and messages deleted.")
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

        room_key = join_chat_room(collection, username, CHAT_ROOM, passcode)
        if room_key is None:
            return

        listener_thread = threading.Thread(target=message_listener, args=(collection, username, room_key))
        listener_thread.daemon = True
        listener_thread.start()

        while True:
            message = input()
            if message.lower() == '/quit':
                break
            send_message(collection, username, message, room_key)

        leave_chat_room(collection, username)
        client.close()

    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    main()