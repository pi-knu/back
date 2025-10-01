FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY alembic.ini .
COPY myapp/ ./myapp/
COPY models.py .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["alembic"]