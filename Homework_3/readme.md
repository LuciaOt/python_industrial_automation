---

This project creates **3 Docker containers** that work together to extract, store, and serve welding data.

## Quickstart

1. **Create a `.env` file** (I did not commit this file) with the following variables:

```
MONGO_HOST=container_name
MONGO_USER=user_name
MONGO_PASS=your_password
MONGO_DB=database_name
MONGO_COLLECTION=data_name

```

2. **Build and start the containers** from the folder containing `docker-compose.yml`:

```bash
docker-compose up -build
```

3. **Inspect the Docker network** if needed:

```bash
docker network inspect my-etl-network
```

4. **Access MongoDB data**:

```bash
docker exec -it mongodb-container mongosh -u admin -p {password} --authenticationDatabase admin
```

> Replace `{password}` with your `.env` value.

Once in the MongoDB shell, you can run (based on what you want to see):

```javascript
use welding_db
show collections
db.welding_data.find().limit(5).pretty()
db.welding_data.findOne()
db.welding_data.countDocuments()
exit
```

5. **Access the Flask API**:

```bash
curl http://localhost:5000/
```

This will return welding data as a Pandas table.

---

## Docker Network

* A custom Docker network `my-etl-network` connects all containers.
* The project includes three containers:

  * **MongoDB Container** – stores the data
  * **Python ETL Container** – reads CSV files and inserts data into MongoDB
  * **Flask API Container** – serves data via a web API

> You can also use the VS Code MongoDB extension to view and explore the database in a user-friendly way.

