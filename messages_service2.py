from fastapi import FastAPI
import pika
import threading
import consul


app = FastAPI()


def register_service(port):
    c = consul.Consul()
    check_http = consul.Check.http(f'http://192.168.65.2:{port}/health', interval='2s')
    c.agent.service.register('messages_service',
                             service_id=f'meassages_service_{port}',
                             address='http://127.0.0.1',
                             port=int(port),
                             check=check_http
                             )


def run_in_thread(fn):
    def run(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
        return t
    return run


@run_in_thread
def consume_loop():
    c = consul.Consul()
    _, rabbit_host = c.kv.get('rabbit_host')
    _, queue_name = c.kv.get('queue_name')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host['Value'].decode().strip('"'))
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name['Value'].decode().strip('"'))
    for method_frame, properties, body in channel.consume(queue_name['Value'].decode().strip('"')):
        print(str(body))
        MSG_LIST.append(str(body))
        print('msg_list', MSG_LIST)


@app.get("/health", status_code=200)
def message_handler():
    return True


@app.get("/lab2")
def root():
    print(MSG_LIST)
    return str(MSG_LIST)


MSG_LIST = []
consume_loop()
register_service(8021)

