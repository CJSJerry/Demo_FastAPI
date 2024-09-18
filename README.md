# Building API for a relational database
Feedback more than welcome; please reach me, Jerry, at CJJerryShieh@gmail.com.

## Technology
- Database: Postgres + pgadmin + docker-compose
- REST API: FastAPI + pytest + Docker
- Diagrams: https://dbdiagram.io/

## Context
Given a mockup relational database with 5 tables, build a REST API to facilitate the connection to other tools and services. \
_Disclaimer_: The sample data and `docker-compose.yml` is by `flvndh`, taken from this repo: https://github.com/flvndh/awesome-inc

## Directory structure
- To start the database: `docker-compose.yml`, `data/`
- For the API: `main.py`, `dependencies.py`, `models/`, `crud/`, `endpoints/`, `test/`
Please see the [structure.md](structure.md) file for the full directory structure.

## Setup

### Part 0: Create environment
1. Clone this repo and `cd` into it
2. Create a virtual environment with **python 3.12.3** and **pip 24.0**, and then activate it 
3. Run `pip install -r requirements.txt` to install all the dependencies

### Part 1: Connect to the database
1. Create an .env file with the url to the database: \
`DATABASE_URL=postgresql://{username}:{password}@host.docker.internal:5432/demo_db` \
Replace the placeholders with your own postgres credentials 
- Credentials will not be found in documentations in real-life scenarios, but for the purpose of this demo, simply copy-paste: `DATABASE_URL=postgresql://demo_user:demo_pw@host.docker.internal:5432/demo_db`
2. Run `docker-compose up -d` to start the database
3. Go to http://localhost:8080 and login with your credentials to access pgadmin 
- For the purpose of this demo, use the following pgadmin credentials as given in `docker-compose.yml`: \
`email: demo_user@test.com` \
`password: demo_pw`
4. Set up the server on pgadmin by going to the left-panel, right-clicking the "Servers" node and select "Create" -> "Server" \
Then, in the "Connection" tab, use the following configuration: \
`Host name/address: postgres` \
`Port: 5432` \
`Username: demo_user` \
`Password: demo_pw` 
- (These postgres credentials follow `docker-compose.yml`, and should not be documented in real-life scenarios)
- (This setup only needs to be done when setting up the database for the first time)
5. Check out the 5 pre-existing tables aunder the "demo_db" database > Schemas > Public > Tables

    <img src="./assets/database.png" alt="Database Image" width="800"/>

### Part 2: Run and test the containerized API
1. Build the docker image \
`docker build -t demo_db-api .`
2. Run a docker container of this image with the correct environment variables \
`docker run --name demo_db-api-app --env-file .env -p 8000:8000 demo_db-api`
- On re-run, use `docker start demo_db-api-app` instead
3. Go to http://localhost:8000/docs to try out the API, with endpoints for all 5 tables, each with 6 HTTP methods

    <img src="./assets/api.png" alt="API Image" width="800"/>

4. Test all possible response codes for all endpoints of all tables by running `pytest -v`, and verify that all 70 tests pass

### Part 3: Clean up
1. Stop the container for API by running `docker stop demo_db-api-app`
2. Stop the database by running `docker-compose down`
3. Deactivate the virtual environment by running `deactivate`

## Contact
Jerry Shieh \
https://www.linkedin.com/in/cjjs/ \
CJJerryShieh@gmail.com