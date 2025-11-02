This project creates 3 Docker containers that work together:

MongoDB Container - Database to store data
Python Container - Reads CSV files and stores data in MongoDB
Flask Container - Web API to retrieve and display stored data

All containers are connected via a Docker network my-first-network

I also added VS Code MongoDB extension setup to my vsc to be able to check what is in the database in more friendly way.



To check the data in the mongodb from python-transformer in powershell, run:

docker exec -it mongodb-container mongosh -u admin -p password123 --authenticationDatabase admin
use welding_db
show collections
db.welding_data.find().limit(5).pretty()





How to build containers

Mongodb 
docker network create my-first-network
docker run -d --name mongodb-container --network my-first-network -p 27017:27017 mongo:latest

Pyton container
From the folder of python container run:
docker build -t python-transformer .
  ```

  *(Dockerfile copies `transform_data.py`, `requirements.txt`, and `datasets/`)*

Run Python container to transform data
docker run --rm --network my-first-network --env-file .env python-transformer 
docker network inspect only shows currently running containers attached to that network. Once the Python container exits and is removed, it disappears from the network list.






Check MongoDB data

docker exec -it mongodb-container mongosh -u admin -p password123 --authenticationDatabase admin
use welding_db
show collections
db.welding_data.find().limit(5).pretty()




After refresh of the connection I can see the data in mongodb vsc extension welding_db is added with welding data in json format 

To check what is in docker network run
docker network inspect my-first-network


FLASH

docker build -t flask-welding-api .

docker run -d `
  --name flask-api `
  --network my-first-network 
  --env-file .env `
  -p 5000:5000 `
  flask-welding-api
