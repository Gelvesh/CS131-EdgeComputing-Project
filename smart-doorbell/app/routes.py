from flask import render_template, Response
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