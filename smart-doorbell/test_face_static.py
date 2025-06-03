import face_recognition
import cv2
import os

# Load known face
known_image = face_recognition.load_image_file("brandon.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Load unknown image to test against
test_image = face_recognition.load_image_file("rachel.jpg")
test_locations = face_recognition.face_locations(test_image)
test_encodings = face_recognition.face_encodings(test_image, test_locations)

# Run comparison
for i, face_encoding in enumerate(test_encodings):
    results = face_recognition.compare_faces([known_encoding], face_encoding)
    print(f"Face {i+1}: {'Match' if results[0] else 'No match'}")

# Optional: Save result with rectangle
output = test_image.copy()
for (top, right, bottom, left) in test_locations:
    cv2.rectangle(output, (left, top), (right, bottom), (0, 255, 0), 2)

# Convert from RGB to BGR before saving
output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
cv2.imwrite("alert_image/result.jpg", output)

print("Saved annotated image to alert_image/result.jpg")