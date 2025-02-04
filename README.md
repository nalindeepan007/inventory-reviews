# inv-reviews
 

#FastAPI-based backend application implementing a review management system with asynchronous task handling using Celery-Redis. The application provides endpoints to fetch review trends and category-specific reviews while maintaining an asynchronous access log.

Features

Implements a relational database schema for managing review history, categories, and access logs using SQLAlchemy .
Provides an API to fetch the top 5 review categories based on average star ratings.
Implements cursor pagination to fetch category-specific reviews sorted by the latest edits.
Uses openapi api to determine sentiment and tone for reviews.

Saves API access logs asynchronously using Celery-redis.

## steps to install 
save a .env file with these values, postgresdb URL, your openapikey, and gpt model to choose from
![image](https://github.com/user-attachments/assets/e7335419-9a90-4ef6-80ae-9a4874df96a7) 

bring up redis referring to the docker file: docker compose up -d \
![image](https://github.com/user-attachments/assets/280dd2c9-3c1a-4945-8d2a-aca2928f0ad1) \

install python dependencies: pip install -r requirements.txt \
start the backend fastapi server: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload \
initiate celery: celery -A celery_worker.celery_app worker --loglevel=info \
(on windows: celery -A celeryLogWorker.celeryLog worker --loglevel=INFO --pool=threads) 

project structure \
![image](https://github.com/user-attachments/assets/3aa6d172-514e-4036-b403-0a7c99b6f1da)
