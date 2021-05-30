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
c = consul.Consul()
_, HZ_node1 = c.kv.get('HZ_node1')
_, HZ_node2 = c.kv.get('HZ_node2')
_, HZ_node3 = c.kv.get('HZ_node3')
_, HZ_map = c.kv.get('HZ_map')


print(HZ_node1['Value'].decode().strip('"'),
        HZ_node2['Value'].decode().strip('"'),
        HZ_node3['Value'].decode().strip('"'))


def register_service(port):
    c = consul.Consul()
    check_http = consul.Check.http(f'http://192.168.65.2:{port}/health', interval='2s')
    c.agent.service.register('logging_service',
                             service_id=f'logging_service_{port}',
                             address='http://127.0.0.1',
                             port=int(port),
                             check=check_http
                             )


client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        HZ_node1['Value'].decode().strip('"'),
        HZ_node2['Value'].decode().strip('"'),
        HZ_node3['Value'].decode().strip('"')

    ]
)

my_map = client.get_map(HZ_map['Value'].decode())


@app.get("/health", status_code=200)
def message_handler():
    return True


@app.post("/lab2", status_code=200)
def handle_message(message: Message):
    my_map.put(message.id, message.msg)
    print(message)


@app.get("/lab2")
def return_messages():
    print([(uid, msg) for (uid, msg) in my_map.entry_set().result()])
    return str([(uid, msg) for (uid, msg) in my_map.entry_set().result()])


if __name__ == "__main__":
    print(sys.argv[1])
    register_service(sys.argv[1])
    uvicorn.run("logging_service:app", port=sys.argv[1])

