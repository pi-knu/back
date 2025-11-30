import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

load_dotenv()

class MinioClient:
    def __init__(self):
        self.endpoint = os.getenv("MINIO_ENDPOINT")
        self.access_key = os.getenv("MINIO_ACCESS_KEY")
        self.secret_key = os.getenv("MINIO_SECRET_KEY")
        self.secure = os.getenv("MINIO_SECURE")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")
        
        self.client = None
        self.connect()

    def connect(self):
        """Establishes connection with minio server"""
        try:
            self.client = Minio(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure
            )
            print(f"[Lots Service] MinIO Client configured for endpoint: {self.endpoint}")
        except Exception as e:
            print(f"[Lots Service] CRITICAL ERROR: Failed to initialize MinIO client: {e}")

    def setup_bucket(self):
        """
        Checks whether bucket exists or doesn't
        """
        if not self.client:
            print("[Lots Service] Error: Client not initialized.")
            return False
            
        try:
            found = self.client.bucket_exists(self.bucket_name)
            if not found:
                self.client.make_bucket(self.bucket_name)
                print(f"[Lots Service] Created new bucket: '{self.bucket_name}'")
            else:
                print(f"[Lots Service] Bucket '{self.bucket_name}' already exists.")
            return True
        except S3Error as e:
            print(f"[Lots Service] MinIO S3 Error: {e}")
            return False
        except Exception as e:
            print(f"[Lots Service] General Error checking bucket: {e}")
            return False

minio_client = MinioClient()