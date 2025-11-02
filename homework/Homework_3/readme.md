This project creates 3 Docker containers that work together:

MongoDB Container - Database to store data
Python Container - Reads CSV files and stores data in MongoDB
Flask Container - Web API to retrieve and display stored data

All containers are connected via a Docker network.

🔐 Important Credentials
MongoDB Database

Username: admin
Password: password123
Port: 27017
Host (from other containers): mongodb-container
Host (from your computer): localhost

Connection String
mongodb://admin:password123@mongodb-container:27017/
(Use this from Python/Flask containers)
mongodb://admin:password123@localhost:27017/
(Use this from your computer)
