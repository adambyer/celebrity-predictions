# Celebrity Predictions

## Create and activate a virtual environment

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`$ pip install -r api/requirements.txt`

## Setup Database

Launch Postgres App, start a PostgreSQL v14 server, and create the `celebrity_predictions` database.

## Install Redis
https://redis.io/

## Migrations

#### Create migrations
`$ alembic revision --autogenerate -m "explain changes"`

#### Apply migrations
`$ alembic upgrade head`

#### Get Migration History
`$ alembic history`

#### Get Current Revision
`$ alembic current`

#### Downgrade to Specific Revision
`$ alembic downgrade <revision>`

## Run the app

#### Redis
`$ redis-server`

#### RabbitMQ (if task_always_eager is False)
`$ rabbitmq-server`

#### Celery (if task_always_eager is False)
`$ source venv/bin/activate`
`$ celery -A api worker -l info`

#### Celery Beat
`$ source venv/bin/activate`
`$ celery -A api beat`

#### Admin
`$ source venv/bin/activate`
`$ cd api`
`$ flask run --port=5001`

#### API
`$ source venv/bin/activate`
`$ uvicorn api.main:app --reload`

#### Frontend
`$ cd frontend`
`$ npm install`
`$ npm run dev`

#### Build Frontend
`$ npm run build`
