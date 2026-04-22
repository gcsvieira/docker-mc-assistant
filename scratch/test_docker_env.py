import os
import docker

# Simulate environment variable set by Docker Compose
os.environ["DOCKER_HOST"] = "tcp://localhost:2375"

try:
    client = docker.from_env()
    print(f"Client base_url: {client.api.base_url}")
    if client.api.base_url == "http://localhost:2375/":
        print("SUCCESS: docker.from_env() picks up DOCKER_HOST.")
    else:
        print(f"FAILURE: Unexpected base_url {client.api.base_url}")
except Exception as e:
    print(f"Error: {e}")
