import docker
import time

client = docker.from_env(timeout=5)
try:
    container_list = client.containers.list(all=True)
    if not container_list:
        print("No containers found!")
    else:
        container = container_list[0]
        print(f"Streaming logs for {container.name} with 5s timeout...")
        # We use a short tail so we don't get flooded
        for line in container.logs(stream=True, follow=True, tail=1):
            print(line)
except Exception as e:
    print(f"Caught exception: {type(e).__name__}: {e}")
