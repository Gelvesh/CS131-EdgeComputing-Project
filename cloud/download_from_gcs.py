# cloud/download_from_gcs.py

from google.cloud import storage
import os

BUCKET_NAME = "cs131project-bucket"
DEST_DIR = "downloaded"
os.makedirs(DEST_DIR, exist_ok=True)

def download_blob(blob_name, local_path):
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        print(f" Downloaded {blob_name} to {local_path}")
    except Exception as e:
        print(f"✗ Failed to download {blob_name}: {e}")

if __name__ == "__main__":
    download_blob("encrypted_image.bin", os.path.join(DEST_DIR, "encrypted_image.bin"))
    download_blob("encrypted_log.txt", os.path.join(DEST_DIR, "encrypted_log.txt"))
