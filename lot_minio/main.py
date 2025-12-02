import time
from minio_client import minio_client

if __name__ == "__main__":
    print("[Lots Service] Starting Lots Service...")
    
    time.sleep(5)
    
    success = minio_client.setup_bucket()
    
    if success:
        print("[Lots Service] Successfully connected to MinIO storage.")
    else:
        print("[Lots Service] WARNING: Could not connect to MinIO.")

    print("[Lots Service] Service is running and waiting for tasks...")
    while True:
        time.sleep(60)