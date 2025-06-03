Steps to Run/Test the Smart Doorbell with Face Recognition

1. Create a Virtual Environment

Command to create a virtual environment:

Linux: python3 -m venv venv310

Windows: python -m venv venv310

To activate the virtual environment:

Linux: source venv310/bin/activate

Windows: venv310\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

Alternatively, install required packages manually:
pip install face_recognition opencv-python

Refer to this guide to install the dlib and face_recognition libraries if needed:
https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f

2. Prepare Image Data

Place clear, frontal images of the individuals you want the system to recognize (e.g., brandon.jpg, rachel.jpg) in the working directory.

Update face_detect.py to reference the new image files and names as needed.

3. Prepare Project Directories

Ensure the following directories are present and empty before starting:

alert_image

encrypted

logs

downloaded

decrypted

4. Run the Camera System

From the project root, run:
python face_detect.py

This will :

Display video window and labels

Accessible remotely via http://[Host-IP]:5000 on any smartphone/PC browser

Alert you by email (with an attached image) when an unknown is seen (no spam)

alert_image/alert.jpg when an unknown face is detected

logs/alert_log.txt containing timestamps

Safely clean up after itself

5. Set Google Cloud Credentials and create a Google Cloud service account key

Create a google cloud account

Go to- https://console.cloud.google.com/
Use the dropdown at the top left to choose cs131project or the correct project you're working on.
Go to “IAM & Admin” → “Service Accounts”
Click “Create Service Account”
Service account name: e.g., edge-computing-uploader
Grant this service account access to the project -> Continue -> Done
Find your new service account in the list.
Go to navigation menu
Manage keys -> Add Key -> Create new key -> Choose JSON, then Create
A .json file will be downloaded to your computer — add it to the project directory
 
Run the following command (adjust the path to your credentials JSON file)(This command is for Windows):
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\rishika\masters\q3\cs131\project\main\CS131-EdgeComputing-Project\cs131project-461300-7c6d4e93b117.json"
6. Encrypt and Upload to Cloud

Use the generated alert image and log file for encryption and upload:
python cloud/encrypt_utils.py
python cloud/upload_gcs.py

If needed, reset the credentials before continuing:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\rishika\masters\q3\cs131\project\main\CS131-EdgeComputing-Project\cs131project-461300-7c6d4e93b117.json"

They can be viewed here- "https://console.cloud.google.com/storage/browser/cs131project-bucket;tab=objects?forceOnBucketsSortingFiltering=true&inv=1&invt=AbywxA&project=cs131project-461300&prefix=&forceOnObjectsSortingFiltering=false"

7. Download Encrypted Data from Cloud

Run:
python cloud/download_from_gcs.py
This will save the files as:

downloaded/encrypted_image.bin

downloaded/encrypted_log.txt

8. Decrypt the Downloaded Files

Run:
python cloud/decrypt_utils.py
This will output:

decrypted/decrypted_image.bin

decrypted/decrypted_log.txt



