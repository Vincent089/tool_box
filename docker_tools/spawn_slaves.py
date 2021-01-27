import docker

# gets the local docker service
client = docker.from_env()

container = client.containers.run('python:3.6-slim',
                                  command=r'python --version',
                                  detach=True)
print(container.logs())
