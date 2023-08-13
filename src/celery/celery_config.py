from src.config import settings

broker_url = settings.BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

imports = ('src.celery.tasks',)

task_track_started = True
broker_connection_retry_on_startup = True
