from fastapi import FastAPI
from pydantic import BaseModel


class Message(BaseModel):
    id: str
    msg: str


app = FastAPI()

hash_table = dict()


@app.post("/lab2", status_code=200)
def handle_message(message: Message):
    hash_table[message.id] = message.msg
    print(message)


@app.get("/lab2")
def return_messages():
    return ''.join(hash_table.values())

