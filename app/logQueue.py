from celery import Celery
from app.dbModel import AccessLog
from app.dbLogging import SessionLocal



celeryLog = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

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