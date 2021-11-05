from celery import Celery


app = Celery("predictions")
app.config_from_object("api.celery_config")
