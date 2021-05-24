import hazelcast

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ]
)
my_map = client.get_map("lab3_4")
key = '1'
my_map.put(key, 0)
print('starting')
for i in range(1000):
    while True:
        old_value = my_map.get(key).result()
        new_value = int(old_value) + 1
        if my_map.replace_if_same(key, old_value, new_value):
            break

print(" Optimistic locking Finished! Result = " + str(my_map.get(key).result()))
