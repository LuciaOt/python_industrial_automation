# Welding Data ETL Project

This project creates **3 Docker containers** that work together to extract, store, and serve welding data.

## Quickstart

1. Create a `.env` file with the following variables (do not commit this file):
   MONGO_HOST=
   MONGO_PORT=
   MONGO_DB=
   MONGO_COLLECTION=

2. Build and start the containers from the folder containing `docker-compose.yml`:
   docker-compose up -d

3. Inspect the Docker network if needed:
   docker network inspect my-etl-network

4. Access MongoDB data:
   docker exec -it mongodb-container mongosh -u admin -p {password} --authenticationDatabase admin
   (Replace `{password}` with your `.env` value.) Then in the shell (depending on what you want to see):
   use welding_db
   show collections
   db.welding_data.find().limit(5).pretty()
   db.welding_data.findOne()
   db.welding_data.countDocuments()
   exit

5. Access the Flask API:
   curl [http://localhost:5000/](http://localhost:5000/)
   This returns welding data as a Pandas table.

## Docker Network

* A custom Docker network `my-etl-network` connects all containers.
* The project includes three containers:

  * **MongoDB Container** – stores the data
  * **Python ETL Container** – reads CSV files and inserts data into MongoDB
  * **Flask API Container** – serves data via a web API

VS Code MongoDB extension can also be used to view and explore the database in a user-friendly way.
