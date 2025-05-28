from app import create_app
from app.models import init_db
import threading

def start_face_detection():
    # Importing inside the function to avoid blocking Flask app
    import app.services.face_detect

# Create the Flask app
app = create_app()

# Initialize database
init_db()

# Start face detection in a background thread
detection_thread = threading.Thread(target=start_face_detection, daemon=True)
detection_thread.start()

if __name__ == '__main__':
    # Start the Flask server
    app.run(host='0.0.0.0', port=5000)
