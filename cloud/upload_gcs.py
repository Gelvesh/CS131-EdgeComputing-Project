# cloud/upload_gcs.py

from google.cloud import storage
import os

BUCKET_NAME = "cs131project-bucket"
ENC_IMAGE_PATH = "encrypted/encrypted_image.bin"
ENC_LOG_PATH = "encrypted/encrypted_log.txt"

def upload_blob(source_file_name, destination_blob_name):
    if not os.path.exists(source_file_name):
        print(f"File not found: {source_file_name}")
        return

    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f"Uploaded {source_file_name} → gs://{BUCKET_NAME}/{destination_blob_name}")
    except Exception as e:
        print(f"Failed to upload {source_file_name}: {e}")

if __name__ == "__main__":
    upload_blob(ENC_IMAGE_PATH, "encrypted_image.bin")
    upload_blob(ENC_LOG_PATH, "encrypted_log.txt")
