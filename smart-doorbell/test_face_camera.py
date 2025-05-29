import cv2
import face_recognition
import numpy as np

# Load known faces
known_face_encodings = []
known_face_names = []

# Load Brandon
brandon_image = face_recognition.load_image_file("brandon.jpg")
brandon_encoding = face_recognition.face_encodings(brandon_image)[0]
known_face_encodings.append(brandon_encoding)
known_face_names.append("Brandon")

# Load Rachel
rachel_image = face_recognition.load_image_file("rachel.jpg")
rachel_encoding = face_recognition.face_encodings(rachel_image)[0]
known_face_encodings.append(rachel_encoding)
known_face_names.append("Rachel")

# Initialize webcam (0 is usually the default USB cam)
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Cannot open camera")
    exit()

print("✅ Camera started. Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Resize frame to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # BGR to RGB

    # Detect faces and compare
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Draw a box around the face and label it
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Show the frame
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
