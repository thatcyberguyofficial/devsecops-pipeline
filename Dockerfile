FROM python:3.11.9

WORKDIR /app
COPY . /app
RUN mkdir -p /app/static
COPY static/style.css /app/static/
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
