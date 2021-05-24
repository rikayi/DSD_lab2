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
for i in range(20):
    print(queue.add(i).result())
    print('Producing: ' + str(i))
    time.sleep(0.5)
queue.add(-1)
print('Producer finished')



