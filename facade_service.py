import uuid
import httpx
import json
import random
from fastapi import FastAPI


app = FastAPI()

LOGGING_HOSTS = ('http://127.0.0.1:8011/lab2',
                 'http://127.0.0.1:8012/lab2',
                 'http://127.0.0.1:8013/lab2')

MESSAGES_HOST = 'http://127.0.0.1:8002/lab2'


def get_logging_service():
    return random.choice(LOGGING_HOSTS)


@app.post("/lab2", status_code=200)
def message_handler(msg: str):
    httpx.post(get_logging_service(), data=json.dumps({'id': str(uuid.uuid4()), 'msg': msg}))


@app.get("/lab2")
def message_handler():
    logging_resp = httpx.get(get_logging_service())
    messages_resp = httpx.get(MESSAGES_HOST)
    return logging_resp.text.strip('"') + messages_resp.text.strip('"')


