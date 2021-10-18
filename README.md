# Celebrity Predictions

## Create and activate a virtual environment

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`$ pip install -r requirements.txt`

## Setup Database

Launch Postgres App and start a PostgreSQL v14 server, then...

`$ python3`

`> from .db import db`

`> db.create_all()`

## Install Redis
https://redis.io/

## Migrations

#### Create migrations
`$ flask db migrate -m "explain changes"`
#### Apply migrations
`$ flask db upgrade`

## Run the app

`$ redis-server`
`$ flask run`