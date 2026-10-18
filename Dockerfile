FROM python:3.14-slim

WORKDIR /content

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs

RUN mkdir -p /content && touch /content/data.db

VOLUME ["/content"]

EXPOSE 7999 7998

CMD ["python", "main.py"]
