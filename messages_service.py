from fastapi import FastAPI
import pika
import threading
import consul
import sys
import uvicorn

def run_in_thread(fn):
    def run(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
        return t
    return run


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    data.append(body)
    print(data)


@run_in_thread
def consume_loop(messages_list):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='lab6_1')
    for method_frame, properties, body in channel.consume('lab6_1'):
        print(str(body))
        messages_list.append(str(body))


data = []
consume_loop(data)
app = FastAPI()


@app.get("/lab2")
def root():
    print(data)
    return str(data)


if __name__ == "__main__":
    print(sys.argv[1], sys.argv[2])
    uvicorn.run("logging_service:app", port=sys.argv[1])
