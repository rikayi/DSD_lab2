import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.queue_declare(queue='limit', arguments={'x-max-length': 5})

channel.queue_declare(queue='limit_reject', arguments={'x-max-length': 5,  'x-overflow': 'reject-publish'})

channel.queue_declare(queue='persistent_queue', durable=True)
#, properties=pika.BasicProperties(delivery_mode=2)

channel.queue_declare(queue='ttl_queue', arguments={'x-message-ttl': 10000})

channel.queue_declare(queue='ack_queue')


for i in range(10):
    time.sleep(1)
    msg = f'msg{i}'
    print(f'[x] Sent {msg}')
    channel.basic_publish(exchange='', routing_key='ttl_queue', body=msg, properties=pika.BasicProperties(delivery_mode=2))
connection.close()
