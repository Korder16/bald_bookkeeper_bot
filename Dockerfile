FROM python:3.11-slim

WORKDIR /usr/src/bot

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "bot.py"]