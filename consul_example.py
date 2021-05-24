import consul

c = consul.Consul()

# poll a key for updates
index, services = c.health.service('restapi', passing=True)


for service_info in services:
    service = service_info['Service']
    print(service)