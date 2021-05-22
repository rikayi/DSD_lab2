import uuid
import httpx
import json
import random
from fastapi import FastAPI
import pika


app = FastAPI()

LOGGING_HOSTS = ('http://127.0.0.1:8011/lab2',
                 'http://127.0.0.1:8012/lab2',
                 'http://127.0.0.1:8013/lab2')

MESSAGES_HOSTS = ('http://127.0.0.1:8002/lab2',
                  'http://127.0.0.1:8003/lab2')


def get_logging_service():
    return random.choice(LOGGING_HOSTS)


def get_messages_service():
    return random.choice(MESSAGES_HOSTS)


@app.post("/lab2", status_code=200)
def message_handler(msg: str):
    httpx.post(get_logging_service(), data=json.dumps({'id': str(uuid.uuid4()), 'msg': msg}))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='lab6_1')
    channel.basic_publish(exchange='', routing_key='lab6_1', body=msg)
    connection.close()


@app.get("/lab2")
def message_handler():
    logging_resp = httpx.get(get_logging_service())
    messages_resp = httpx.get(get_messages_service())
    return logging_resp.text.strip('"') + '\n' + messages_resp.text.strip('"')


