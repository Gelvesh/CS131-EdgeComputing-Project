from flask import render_template, Response
from .models import init_db, log_visitor
import time
import app.services.face_detect as face_detect  # adjust if path differs

def init_routes(app):
    @app.route('/')
    def dashboard():
        return render_template('dashboard.html')

    def gen_frames():
        while True:
            frame = face_detect.get_latest_frame()
            if frame is None:
                time.sleep(0.1)
                continue
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/visitors')
    def show_visitors():
        import sqlite3
        conn = sqlite3.connect('visitors.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        visitors = c.execute('SELECT * FROM visitors ORDER BY timestamp DESC').fetchall()
        conn.close()
        return render_template('visitors.html', visitors=visitors)
