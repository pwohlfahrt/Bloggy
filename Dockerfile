FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs
RUN mkdir -p content/photos

RUN touch data.db

EXPOSE 8000 7999

CMD ["python", "main.py"]
