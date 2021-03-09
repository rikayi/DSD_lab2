import uuid
import httpx
import json
from fastapi import FastAPI


app = FastAPI()

LOGGING_HOST = 'http://127.0.0.1:8001/lab2'
MESSAGES_HOST = 'http://127.0.0.1:8002/lab2'


@app.post("/lab2", status_code=200)
def message_handler(msg: str):
    httpx.post(LOGGING_HOST, data=json.dumps({'id': str(uuid.uuid4()), 'msg': msg}))


@app.get("/lab2")
def message_handler():
    logging_resp = httpx.get(LOGGING_HOST)
    messages_resp = httpx.get(MESSAGES_HOST)
    return logging_resp.text.strip('"') + messages_resp.text.strip('"')


