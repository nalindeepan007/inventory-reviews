from app.logQueue import celeryLog

if __name__ == '__main__':
    celeryLog.worker_main()


# celery -A celeryLogWorker.celeryLog worker --loglevel=INFO --pool=threads