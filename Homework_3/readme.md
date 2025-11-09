This project creates 3 Docker containers that work together:

I created docker network my-etl-netwrok
Credentials are stored in the .env file that i have not commited to git. I stored there MONGO_HOST, MONGO_PORT, MONGO_DB and MONGO_COLLECTION

docker-compose up -d (from the folder where docker-compose.yml is)

<!-- to create network - docker network create my-first-network -->
to inspect my network - docker network inspect my-etl-network




MongoDB Container - Database to store data
Python Container - Reads CSV files and stores data in MongoDB
Flask Container - Web API to retrieve and display stored data

All containers are connected via a Docker network 

I also added VS Code MongoDB extension setup to my vsc to be able to check what is in the database in more friendly way. 



To check the data in the mongodb from python-transformer in powershell, run:
docker exec -it mongodb-container mongosh -u admin -p {password} --authenticationDatabase admin    
(you can use mongosh - MongoDB shell. Add password from the .env to instead of {password})
use welding_db
show collections
db.welding_data.find().limit(5).pretty()
db.welding_data.findOne()
db.welding_data.countDocuments()
.... 
exit





Flask api 
wild get the data from db. 
checl them from 
curl http://localhost:5000/

get the data from welding db 





Run Python container to transform data
docker run --rm --network my-first-network --env-file .env python-transformer 
docker network inspect only shows currently running containers attached to that network. Once the Python container exits and is removed, it disappears from the network list.










After refresh of the connection I can see the data in mongodb vsc extension welding_db is added with welding data in json format 



FLASH

docker build -t flask-welding-api .

docker run -d `
  --name flask-api `
  --network my-first-network 
  --env-file .env `
  -p 5000:5000 `
  flask-welding-api
