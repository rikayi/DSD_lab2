import hazelcast
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import uvicorn
import consul


class Message(BaseModel):
    id: str
    msg: str


app = FastAPI()


def register_service(port):
    c = consul.Consul()
    check_http = consul.Check.http(f'http://192.168.65.2:{port}/health', interval='2s')
    c.agent.service.register('facade_service',
                             service_id=f'facade_service_{port}',
                             port=port,
                             check=check_http
                             )

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        f"127.0.0.1:{sys.argv[2]}"
    ]
)

my_map = client.get_map("lab6_1")


@app.post("/lab2", status_code=200)
def handle_message(message: Message):
    my_map.put(message.id, message.msg)
    print(message)


@app.get("/lab2")
def return_messages():
    print([(uid, msg) for (uid, msg) in my_map.entry_set().result()])
    return str([(uid, msg) for (uid, msg) in my_map.entry_set().result()])


if __name__ == "__main__":
    print(sys.argv[1], sys.argv[2])
    uvicorn.run("logging_service:app", port=sys.argv[1])

