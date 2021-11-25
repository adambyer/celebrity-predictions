from celery.schedules import crontab
import os

# UTC is used by default.

broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://localhost")
include = [
    "api.tasks",
]
beat_schedule = {
    "start-daily-scoring": {
        "task": 'api.tasks.start_daily_scoring',

        # Every day at midnight.
        "schedule": crontab(hour=0, minute=0),
    },
    "import-all-celebrity-daily-metrics": {
        "task": 'api.tasks.import_all_celebrity_daily_metrics',

        # TODO: Every 10 minutes?
        "schedule": crontab(minute="*/10"),
    },
}

task_always_eager = True
