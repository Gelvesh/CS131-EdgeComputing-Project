import face_recognition
import cv2
import time
import os
import threading
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Directory to store alert images
alertDir = "alert_image"
alertfile = 'alert.jpg'
alert_path = os.path.join(alertDir, alertfile)

# Ensure alert directory exists
os.makedirs(alertDir, exist_ok=True)
print("Before saving image:", os.listdir(alertDir))

# === EMAIL SETUP ===
def pushMail(attach_path):
    sender_email = 'ggang004@ucr.edu'
    sender_name = 'Your Name'
    password = 'hpdh rjbu isld ikgo'  # Use Gmail App Password

    receiver_emails = ['ggang004@ucr.edu']
    receiver_names = ['Recipient Name']
    email_body = 'Alert: Unknown person detected! See attached image.'

    for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
        print("Sending the email...")
        msg = MIMEMultipart()
        msg['To'] = formataddr((receiver_name, receiver_email))
        msg['From'] = formataddr((sender_name, sender_email))
        msg['Subject'] = 'UNKNOWN PERSON DETECTED'
        msg.attach(MIMEText(email_body, 'html'))

        # Attach the alert image
        try:
            with open(attach_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attach_path)}",
            )
            msg.attach(part)
        except Exception as e:
            print(f"Attachment error: {e}")
            return

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print('Email sent!')
        except Exception as e:
            print(f'Email sending failed: {e}')
        finally:
            server.quit()

# === Load known faces ===
def load_face_encoding(path, name):
    if not os.path.exists(path):
        print(f"⚠️ Warning: {path} does not exist")
        return None, None
    image = face_recognition.load_image_file(path)
    encs = face_recognition.face_encodings(image)
    if not encs:
        print(f"⚠️ Warning: no face found in {path}")
        return None, None
    return encs[0], name

known_face_encodings = []
known_face_names = []
for img_path, person in [("brandon.jpg", "Brandon"),
                         ("rachel.jpg",  "Rachel")]:
    enc, name = load_face_encoding(img_path, person)
    if enc is not None:
        known_face_encodings.append(enc)
        known_face_names.append(name)

# === Main loop setup ===
video_capture = cv2.VideoCapture(0)

process_this_frame = True
face_locations = []
face_encodings = []
face_names = []

# --- Cooldown timer (avoid email spam) ---
last_alert_time = 0
alert_cooldown = 30  # seconds between alerts

def send_and_delete(path):
    pushMail(path)
    try:
        os.remove(path)
        print("Deleted alert image.")
    except Exception as e:
        print(f"Failed to delete alert image: {e}")

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    # Downsample for speed
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = small_frame[:, :, ::-1]

    if process_this_frame:
        small_locs = face_recognition.face_locations(rgb_small)
        face_locations = [(top*4, right*4, bottom*4, left*4) for
                          (top, right, bottom, left) in small_locs]

        if face_locations:
            face_encodings = face_recognition.face_encodings(frame, face_locations)
        else:
            face_encodings = []

        face_names = []
        for enc in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, enc)
            name = "Unknown"
            if True in matches:
                name = known_face_names[matches.index(True)]
            face_names.append(name)

            # ALERT logic (threaded, no freeze)
            now = time.time()
            if name == "Unknown" and (now - last_alert_time > alert_cooldown):
                print("Who the heck is this?!")
                cv2.imwrite(alert_path, frame)
                print("After saving image:", os.listdir(alertDir))

                threading.Thread(target=send_and_delete, args=(alert_path,), daemon=True).start()

                last_alert_time = now

    process_this_frame = not process_this_frame

    # Draw boxes and labels
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0,0,255), cv2.FILLED)
        cv2.putText(frame, name, (left+6, bottom-6),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255), 1)

    # Show the window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', 600, 600)
    cv2.imshow('Video', frame)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
