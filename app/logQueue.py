from celery import Celery
from app.dbModel import AccessLog
from app.dbLogging import SessionLocal
import os

redisUrl = os.getenv("REDIS_URL")
celeryLog = Celery('tasks', broker=redisUrl, backend=redisUrl)

@celeryLog.task
def logAccess(text: str):
    # sync db setup for celery
    db = SessionLocal()
    try:
        accessLog = AccessLog(text=text)
        db.add(accessLog)
        db.commit()
    finally: 
        db.close()