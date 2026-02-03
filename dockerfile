FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

# Run migrations and start the app
CMD flask db upgrade && flask run --host=0.0.0.0 --port=8080