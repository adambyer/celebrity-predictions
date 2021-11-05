import os

broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://localhost")
include = [
    "api.tasks",
]

task_always_eager = True
