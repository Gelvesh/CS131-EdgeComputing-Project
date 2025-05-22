from flask import render_template, Response
from .models import init_db, log_visitor
import cv2

def init_routes(app):
    @app.route('/')
    def dashboard():
        return render_template('dashboard.html')
    
    def gen_frames():
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success: break
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    @app.route('/video_feed')
    def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    # Add to init_routes function
    @app.route('/visitors')
    def show_visitors():
        conn = sqlite3.connect('visitors.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        visitors = c.execute('SELECT * FROM visitors ORDER BY timestamp DESC').fetchall()
        conn.close()
        return render_template('visitors.html', visitors=visitors)