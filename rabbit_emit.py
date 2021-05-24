import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

for i in range(10):
    msg = f'msg{i}'
    channel.basic_publish(exchange='logs', routing_key='', body=msg)
connection.close()
