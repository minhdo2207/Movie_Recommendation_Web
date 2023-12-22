FROM python:3.12-slim

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

COPY ./requirements.txt .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 5000

COPY . .

# Use Gunicorn to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
