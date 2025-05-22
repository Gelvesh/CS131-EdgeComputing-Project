from app import create_app
from app.models import init_db
import threading
from face_detect import run_face_detection

app = create_app()
init_db()

# Run face detection in background
detection_thread = threading.Thread(target=run_face_detection, daemon=True)
detection_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)