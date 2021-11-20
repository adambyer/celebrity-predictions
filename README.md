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

NOTE: The circular dependencies warning can be ignored... https://github.com/axios/axios/issues/4177

#### Build Frontend
`$ npm run build`

## Do Stuff
Start by adding some celebrities in admin. You only need to set the `twitter_username` field. After saving, the app will fetch the other Twitter fields and update the row.

Next add some predictions, either in the app or in admin.

There's a custom action in celebrity admin to import yesterday's metrics. 

You can also start a shell to run specific methods...

`$ source venv/bin/activate`

`$ python3 -i shell.py`

`>>> from api.scripts import import_metrics`

`>>> import_metrics(3, 1)`

You can also just run `start_daily_scoring` which will import metrics and score predictions for all celebrities for the specified date.