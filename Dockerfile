FROM python:3.11-slim

WORKDIR /usr/src/bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]