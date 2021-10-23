# Celebrity Predictions

## Create and activate a virtual environment

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`$ pip install -r requirements.txt`

## Setup Database

Launch Postgres App, start a PostgreSQL v14 server, and create the `celebrity_predictions` database.

## Install Redis
https://redis.io/

## Migrations

#### Create migrations
`$ alembic revision --autogenerate -m "explain changes"`

#### Apply migrations
`$ alembic upgrade head`

## Run the app

#### Redis
`$ redis-server`

### Admin
`$ flask run`

### API
`$ uvicorn api.main:app --reload`