Steps to test:
1. Software/Packages:
You’ll need the following Python libraries:
face_recognition
opencv-python (cv2)
pip install face_recognition opencv-python

3. Images:
Place clear frontal images of people you want to recognize (e.g., brandon.jpg, rachel.jpg) in your working directory.

4. Make sure an alert_image directory exists:
mkdir alert_image

5. Make sure your image files (brandon.jpg, rachel.jpg) are in the same directory.

6. Run the Code
From your terminal or Anaconda prompt:
python face_alert.py

7. Now, your script will:
Detect faces
Alert you by email (with an attached image) when an unknown is seen (no spam)
Display video window and labels
Safely clean up after itself
