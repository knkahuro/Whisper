#🎴kenny
#06/08/2024

import base64
import pymongo
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
    username = input("Enter codename:")
    password = getpass("Enter password:")
    return username, password

# Function to connect to MongoDB Atlas
def connect_to_mongodb(username, password):
    uri = MONGO_URI.replace("<username>", username).replace("<password>", password)
    client = MongoClient(uri)
    return client

#Function to generate a new Fernet key
def generate_key():
    return Fernet.generate_key()

#function to encrypt message 
def encrypt_message(key, message):
    f = Fernet(key)
    return f.ecrypt(message.encode()).decode() 

#function to decrypt message
def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    return f.decryption(encrypted_message.encode()).decode()

# Function to join chat room
def join_chat_room(collection, username, chat_room):
    room_info = collection.find_one({"_id": chat_room})
    if room_info is None:
        collection.insert_one({"_id": chat_room, "users": [username], "messages": []})
        print("🏳️Created private chat room. Waiting for another user to join...")
    elif len(room_info["users"]) < MAX_CLIENTS and username not in room_info["users"]:
        collection.update_one({"_id": chat_room}, {"$push": {"users": username}})
        print(f"Joined the private chat room with {room_info['users'][0]}")
    else:
        print("Private chat room is full or you're already in it.")
        return None
    
    return base64.urlsafe_b64decode(room_info["room_key"].encode())

# Function to send a message
def send_message(collection, username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        "timestamp": timestamp,
        "username": username,
        "message": encrypt_message
    }
    collection.update_one({"_id": CHAT_ROOM}, {"$push": {"messages": message_data}})
    print(f"sent at {timestamp}")

# Function to retrieve and display new messages
def get_new_messages(collection, last_index):
    room_info = collection.find_one({"_id": CHAT_ROOM})
    messages = room_info["messages"][last_index:]
    for msg in messages:
        print(f"[{msg['timestamp']}] {msg['username']} : {msg['decrypted_message']}")
    return len(room_info["messages"])

# Function to continuously check for new messages
def message_listener(collection, username):
    last_index = 0
    while True:
        last_index = get_new_messages(collection, last_index)
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
    username, password = get_credentials()

    try:
        client = connect_to_mongodb(username, password)
        db = client['chat_database']
        collection = db['chat_collection']
        print(f"Connected to the chat as {username}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return
