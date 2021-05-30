import uuid
import httpx
import json
import random
from fastapi import FastAPI
import pika
import consul
import uvicorn
import sys


app = FastAPI()


def register_service(port):
    c = consul.Consul()
    check_http = consul.Check.http(f'http://192.168.65.2:{port}/health', interval='2s')
    c.agent.service.register('facade_service',
                             service_id=f'facade_service_{port}',
                             address='http://127.0.0.1',
                             port=int(port),
                             check=check_http
                             )


LOGGING_HOSTS = ('http://127.0.0.1:8011/lab2',
                 'http://127.0.0.1:8012/lab2',
                 'http://127.0.0.1:8013/lab2')

MESSAGES_HOSTS = ('http://127.0.0.1:8021/lab2',
                  'http://127.0.0.1:8022/lab2')


def get_logging_service():
    c = consul.Consul()
    index, services = c.health.service('logging_service', passing=True)
    addresses = [service_info['Service']['Address'] + ':' + str(service_info['Service']['Port']) + '/lab2'
                 for service_info in services]
    return random.choice(addresses)


def get_messages_service():
    c = consul.Consul()
    index, services = c.health.service('messages_service', passing=True)
    addresses = [service_info['Service']['Address'] + ':' + str(service_info['Service']['Port']) + '/lab2'
                 for service_info in services]
    return random.choice(addresses)


@app.get("/health", status_code=200)
def message_handler():
    return True


@app.post("/lab2", status_code=200)
def message_handler(msg: str):
    c = consul.Consul()
    _, rabbit_host = c.kv.get('rabbit_host')
    _, queue_name = c.kv.get('queue_name')
    httpx.post(get_logging_service(), data=json.dumps({'id': str(uuid.uuid4()), 'msg': msg}))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host['Value'].decode().strip('"')))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name['Value'].decode().strip('"'))
    channel.basic_publish(exchange='', routing_key=queue_name['Value'].decode().strip('"'), body=msg)
    connection.close()


@app.get("/lab2")
def message_handler():
    logging_resp = httpx.get(get_logging_service())
    messages_resp = httpx.get(get_messages_service())
    return logging_resp.text.strip('"') + '\n' + messages_resp.text.strip('"')


if __name__ == "__main__":
    print(sys.argv[1])
    register_service(sys.argv[1])
    uvicorn.run("facade_service:app", port=sys.argv[1])


