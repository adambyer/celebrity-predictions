from celery import Celery


app = Celery("predictions")
app.config_from_object("api.celery_config")

# This is needed for Admin to create tasks.
app.set_default()
