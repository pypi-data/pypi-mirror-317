from google.cloud import storage
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from io import BytesIO
import os
from typing import Optional

from botrun_flow_lang.constants import HATCH_BUCKET_NAME
from botrun_flow_lang.services.storage.storage_store import StorageStore


class StorageCsStore(StorageStore):
    def __init__(self, env_name: str):
        google_service_account_key_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
            "/app/keys/scoop-386004-d22d99a7afd9.json",
        )
        credentials = service_account.Credentials.from_service_account_file(
            google_service_account_key_path,
            scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
        )

        self.storage_client = storage.Client(credentials=credentials)
        self.bucket_name = f"{HATCH_BUCKET_NAME}-{env_name}"
        self.bucket = self.create_bucket(self.bucket_name)
        if not self.bucket:
            raise Exception(f"Failed to create or get bucket: {self.bucket_name}")

    def create_bucket(self, bucket_name: str) -> Optional[storage.Bucket]:
        """創建新的 bucket，如果已存在則返回現有的"""
        try:
            bucket = self.storage_client.bucket(bucket_name)

            if not bucket.exists():
                print(f"Creating new bucket: {bucket_name}")
                bucket = self.storage_client.create_bucket(
                    bucket_name, location="asia-east1"
                )
                print(f"Created bucket {bucket_name} in asia-east1")
            else:
                print(f"Bucket {bucket_name} already exists")

            return bucket
        except Exception as e:
            print(f"Error creating bucket {bucket_name}: {str(e)}")
            return None

    async def store_file(self, filepath: str, file_object: BytesIO) -> bool:
        try:
            blob = self.bucket.blob(filepath)
            blob.upload_from_file(file_object, rewind=True)
            return True
        except Exception as e:
            print(f"Error storing file in Cloud Storage: {e}")
            return False

    async def retrieve_file(self, filepath: str) -> BytesIO:
        try:
            blob = self.bucket.blob(filepath)
            file_object = BytesIO()
            blob.download_to_file(file_object)
            file_object.seek(0)  # Rewind the file object to the beginning
            return file_object
        except NotFound:
            print(f"File not found in Cloud Storage: {filepath}")
            return None
        except Exception as e:
            print(f"Error retrieving file from Cloud Storage: {e}")
            return None

    async def delete_file(self, filepath: str) -> bool:
        try:
            blob = self.bucket.blob(filepath)
            blob.delete()
            return True
        except NotFound:
            print(f"File not found in Cloud Storage: {filepath}")
            return False
        except Exception as e:
            print(f"Error deleting file from Cloud Storage: {e}")
            return False

    async def file_exists(self, filepath: str) -> bool:
        try:
            blob = self.bucket.blob(filepath)
            return blob.exists()
        except Exception as e:
            print(f"Error checking file existence in Cloud Storage: {e}")
            return False
