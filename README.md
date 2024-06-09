# Whisper
(an ephemeral Encrypted Chat)

## Overview

Ephemeral Encrypted Chat is a simple, secure, and private chat application built with Python. It uses MongoDB Atlas as a cloud-based database and the Fernet encryption scheme to ensure that your messages are confidential.
The chat is ephemeral, meaning all messages are automatically deleted when the chat session ends, providing an extra layer of privacy.

## Features

- *End-to-End Encryption*: All messages are encrypted before being sent to the database and decrypted only on the recipient's device.
- *Ephemeral Messages*: Once all users leave the chat, all messages are permanently deleted.
- *Unique Encryption Keys*: Each chat session generates its own encryption key, ensuring perfect forward secrecy.
- *Cloud-Based*: Uses MongoDB Atlas, allowing users to chat from anywhere without setting up a local database.
- *Two-User Limit*: Designed for private, one-on-one conversations.
- *Real-Time Messaging*: Messages appear instantly on the recipient's screen.
- *Simple Interface*: Easy-to-use command-line interface.

## Prerequisites

- Python 3.6 or newer
- pip (Python package installer)
- A free MongoDB Atlas account

## Installation

1. *Python and pip*:
   - Download and install Python from [python.org](https://www.python.org/downloads/).
   - On Windows, ensure you check "Add Python to PATH" during installation.

2. *MongoDB Atlas Setup*:
   - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a free tier cluster.
   - In "Security" > "Database Access", create a user with read and write privileges.
   - In "Security" > "Network Access", add your IP or allow access from anywhere (0.0.0.0/0) for testing.
   - In "Clusters", click "Connect", choose "Connect your application", and copy the connection string.

3. *Project Setup*:
   - Download encrypted_chat.py, setup_chat.sh (macOS/Linux), and setup_chat.bat (Windows).
   - Place all files in the same directory.
   - Open encrypted_chat.py and replace "your_mongodb_atlas_uri_here" with your connection string.

4. *Install Dependencies*:
   - On macOS/Linux:
     
     chmod +x setup_chat.sh
     ./setup_chat.sh
     
   - On Windows: Double-click setup_chat.bat.

## Usage

1. Open two terminal windows (simulating two users).
2. In each terminal, navigate to the project directory.
3. Run the chat application:
4. When prompted, enter:
- A username (e.g., "Alice" in one terminal, "Bob" in the other)
- The MongoDB user password you created

5. Start chatting:
- Type your message and press Enter to send.
- Messages appear instantly in the other user's terminal.

6. To end the chat:
- Type exit and press Enter in either terminal.
- When both users exit, all messages are permanently deleted.

## Important Notes

- *Security*: 
- Never share your MongoDB Atlas credentials publicly.
- The setup_chat scripts install required packages (pymongo and cryptography) if not already present.

- *Ephemeral Nature*:
- All messages are deleted when the chat ends. There's no chat history or backup.
- Great for privacy, but be mindful if you need to keep records.

- *Two-User Limit*:
- The app is designed for private, one-on-one chats.
- For group chats, you'd need to modify the code.

- *Network Dependency*:
- Both users need internet access to connect to MongoDB Atlas.
- If a user loses connection, they'll need to restart the script.

- *Educational Purpose*:
- This project is great for learning about cloud databases, real-time apps, and basic cryptography.
- It's not production-ready; use it as a learning tool or prototype.

## Troubleshooting

- *Connection Issues*: Ensure your MongoDB Atlas network settings allow your IP.
- *Installation Errors*: Make sure Python and pip are correctly installed and in your PATH.
- *Script Errors*: On some systems, use python3 instead of python.

## Contributing

This is an educational project, but suggestions and improvements are welcome! Feel free to fork the repository, make changes, and submit pull requests❤️.

## License

This project is open-source and available under the MIT License.

---

Enjoy your secure, ephemeral chats! Remember, in the world of this application, what happens in chat, stays in chat... and then vanishes forever! 🕵‍♂💬🔒
