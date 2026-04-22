import os
import sys
import docker

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from ops import docker as docker_ops

def test_label_filtering():
    client = docker.from_env()
    
    # 1. Setup environment
    # Note: ALLOWED_CONTAINERS is no longer used for discovery
    os.environ["MANAGED_LABEL_KEY"] = "mc_assistant.managed"
    os.environ["MANAGED_LABEL_VALUE"] = "true"
    
    # 2. Create test containers
    print("Creating test containers...")
    try:
        client.containers.run("alpine", "sleep 100", name="managed-test", labels={"mc_assistant.managed": "true"}, detach=True)
        client.containers.run("alpine", "sleep 100", name="unmanaged-test", detach=True)
    except Exception as e:
        print(f"Setup error (maybe they exist?): {e}")

    try:
        # 3. Run test
        print("Testing get_allowed_containers()...")
        allowed = docker_ops.get_allowed_containers()
        print(f"Allowed containers: {allowed}")
        
        assert "managed-test" in allowed, "managed-test should be allowed"
        assert "unmanaged-test" not in allowed, "unmanaged-test should NOT be allowed"
        print("✅ get_allowed_containers test passed!")
        
        # 4. Test _get_container enforcement
        print("Testing _get_container enforcement...")
        os.environ["CONTAINER_NAME"] = "managed-test"
        c = docker_ops._get_container()
        print(f"Successfully retrieved {c.name}")
        
        os.environ["CONTAINER_NAME"] = "unmanaged-test"
        try:
            docker_ops._get_container()
            print("❌ Error: _get_container should have raised NotFound for unmanaged-test")
            sys.exit(1)
        except docker.errors.NotFound:
            print("✅ _get_container enforcement test passed!")
            
    finally:
        # Cleanup
        print("Cleaning up...")
        for name in ["managed-test", "unmanaged-test"]:
            try:
                c = client.containers.get(name)
                c.remove(force=True)
            except:
                pass
        print("Done.")

if __name__ == "__main__":
    test_label_filtering()
