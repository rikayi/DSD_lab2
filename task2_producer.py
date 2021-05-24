import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
for i in range(10):
    msg = f'msg{i}'
    print('[x] Sent {msg}')
    channel.basic_publish(exchange='', routing_key='hello', body=msg)


channel.queue_declare(queue='response')
channel.basic_consume(queue='response', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
