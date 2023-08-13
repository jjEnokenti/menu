from celery import Celery
from src.celery import celery_config

app = Celery('tasks')

app.config_from_object(celery_config)
