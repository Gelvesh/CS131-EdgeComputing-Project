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
from datetime import datetime
from flask import Flask, Response, render_template_string

# Initialize Flask app
app = Flask(__name__)
latest_frame = None
frame_lock = threading.Lock()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Face Detection Feed</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; }
        img { width: 100%; border: 2px solid #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Face Detection Live Feed</h1>
        <img src="{{ url_for('video_feed') }}">
    </div>
</body>
</html>
"""

# Flask routes
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    def generate():
        global latest_frame
        while True:
            with frame_lock:
                if latest_frame is None:
                    continue
                ret, buffer = cv2.imencode('.jpg', latest_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask():
    app.run(host='0.0.0.0', port=5000, threaded=True)

# Original face detection setup
os.makedirs("logs", exist_ok=True)
alertDir = "alert_image"
alertfile = 'alert.jpg'
alert_path = os.path.join(alertDir, alertfile)
os.makedirs(alertDir, exist_ok=True)

# === EMAIL SETUP ===
def pushMail(attach_path):
    sender_email = 'cleun042@ucr.edu'
    sender_name = 'Your Name'
    password = 'hpdh rjbu isld ikgo'  # Use Gmail App Password

    receiver_emails = ['cleun042@ucr.edu']
    receiver_names = ['Recipient Name']
    email_body = 'Alert: Unknown person detected! See attached image.'

    for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
        print("Sending the email...")
        msg = MIMEMultipart()
        msg['To'] = formataddr((receiver_name, receiver_email))
        msg['From'] = formataddr((sender_name, sender_email))
        msg['Subject'] = 'UNKNOWN PERSON DETECTED'
        msg.attach(MIMEText(email_body, 'html'))

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
                         ("rachel.jpg",  "Rachel"),
                         ("rishika.jpg", "Rishika")]:
    enc, name = load_face_encoding(img_path, person)
    if enc is not None:
        known_face_encodings.append(enc)
        known_face_names.append(name)

# === Main detection function ===
def detect_faces():
    global latest_frame
    
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    face_locations = []
    face_names = []
    last_alert_time = 0
    alert_cooldown = 30  # seconds between alerts

    while True:
        ret, frame = video_capture.read()
        if not ret:
            continue

        # Update the latest frame for web streaming
        with frame_lock:
            latest_frame = frame.copy()

        # Downsample for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = small_frame[:, :, ::-1]

        if process_this_frame:
            small_locs = face_recognition.face_locations(rgb_small)
            face_locations = [(top*4, right*4, bottom*4, left*4) for
                              (top, right, bottom, left) in small_locs]

            face_encodings = face_recognition.face_encodings(frame, face_locations) if face_locations else []

            face_names = []
            for enc in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, enc)
                name = "Unknown"
                if True in matches:
                    name = known_face_names[matches.index(True)]
                face_names.append(name)

                # ALERT logic
                now = time.time()
                if name == "Unknown" and (now - last_alert_time > alert_cooldown):
                    print("Unknown person detected!")
                    cv2.imwrite(alert_path, frame)
                    threading.Thread(target=send_and_delete, args=(alert_path,), daemon=True).start()
                    last_alert_time = now

        process_this_frame = not process_this_frame

        # Draw boxes and labels
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0,0,255), cv2.FILLED)
            cv2.putText(frame, name, (left+6, bottom-6),
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255), 1)

        # Show the local window
        cv2.imshow('Local Video Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def send_and_delete(path):
    pushMail(path)
    
    os.makedirs("logs", exist_ok=True)
    log_file_path = "logs/alert_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ALERT: Unknown person detected. Image: {path}\n"
    
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry)
        print(f"Log written → {log_file_path}")
    except Exception as e:
        print(f"Failed to write log: {e}")

    def delayed_delete(p, delay=1200):
        time.sleep(delay)
        try:
            os.remove(p)
            print(f"Deleted alert image after {delay} seconds.")
        except Exception as e:
            print(f"Failed to delete alert image: {e}")

    threading.Thread(target=delayed_delete, args=(path,), daemon=True).start()

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start face detection
    detect_faces()