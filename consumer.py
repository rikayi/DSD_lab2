import hazelcast
import time

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ]
)
queue = client.get_queue("q1")
time.sleep(10)
while True:
    item = queue.take().result()
    print('Consumed: ' + str(item))
    time.sleep(1)
    if item==-1:
        print('Consumed -1')
        break

print('Consumer finished')