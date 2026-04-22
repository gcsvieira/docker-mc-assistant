import docker
import sys

def test_operation(name, func):
    print(f"[*] Testing: {name}...", end=" ", flush=True)
    try:
        func()
        print("✅ ALLOWED")
    except docker.errors.APIError as e:
        if e.response.status_code == 403:
            print("❌ BLOCKED (403 Forbidden) - SUCCESS")
        else:
            print(f"❓ FAILED with error: {e}")
    except Exception as e:
        print(f"💥 ERROR: {e}")

def run_suite():
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"Could not connect to Docker: {e}")
        sys.exit(1)

    print("--- Docker Proxy Security Validation ---")
    
    # 1. Test Allowed: List containers
    test_operation("List Containers", lambda: client.containers.list())

    # 2. Test Allowed: Get specific container
    mc_name = "enan-mc" 
    test_operation(f"Inspect container '{mc_name}'", lambda: client.containers.get(mc_name))

    # 3. Test Blocked: List Images
    test_operation("List Images (Should be blocked)", lambda: client.images.list())

    # 4. Test Blocked: List Volumes
    test_operation("List Volumes (Should be blocked)", lambda: client.volumes.list())

    # 5. Test Blocked: List Networks
    test_operation("List Networks (Should be blocked)", lambda: client.networks.list())

    print("\n--- Validation Complete ---")

if __name__ == "__main__":
    run_suite()
