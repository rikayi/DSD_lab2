import hazelcast

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ],
    lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]

)

my_map = client.get_map("lab3").blocking()

for i in range(100):
    my_map.put(str(i), i)

# Shutdown this Hazelcast Client
client.shutdown()
