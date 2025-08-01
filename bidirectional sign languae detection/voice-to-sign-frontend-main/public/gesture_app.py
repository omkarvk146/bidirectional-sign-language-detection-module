from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import os
import absl.logging
from collections import deque
import time
from math import sqrt

# Suppress TensorFlow and absl logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
absl.logging.set_verbosity(absl.logging.ERROR)

app = Flask(__name__)

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
gesture_history = deque(maxlen=10)

sentence = ""
last_gesture = ""
last_detected_time = time.time()

def get_distance(a, b):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def recognize_gesture(hand_landmarks):
    if hand_landmarks:
        landmarks = hand_landmarks.landmark
        # Previous gestures
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y and
            landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x):
            return "Thumbs Up"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.WRIST].y and
            all(landmarks[finger].y < landmarks[finger - 2].y for finger in [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP])):
            return "Hello"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.WRIST].y and
            landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].y < landmarks[mp_hands.HandLandmark.PINKY_PIP].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y):
            return "I Love You"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y > landmarks[mp_hands.HandLandmark.WRIST].y and
            all(landmarks[finger].y < landmarks[finger - 2].y for finger in [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP])):
            return "What"
       
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].y > landmarks[mp_hands.HandLandmark.PINKY_PIP].y):
            return "Are"

        if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x:
            return "How"
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x):
            return "Why"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.WRIST].y and
            landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y):
            return "Thank You"
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].y > landmarks[mp_hands.HandLandmark.PINKY_PIP].y):
            return "Peace"
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.THUMB_TIP].y > landmarks[mp_hands.HandLandmark.THUMB_IP].y):
            return "No"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y > landmarks[mp_hands.HandLandmark.THUMB_IP].y and
            landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y):
            return "Yes"
        # Daily conversation signs
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y):
            return "OK"
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.WRIST].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.WRIST].y):
            return "Good Morning"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].x > landmarks[mp_hands.HandLandmark.WRIST].x and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].x < landmarks[mp_hands.HandLandmark.WRIST].x):
            return "Sorry"
        if (landmarks[mp_hands.HandLandmark.PINKY_TIP].x < landmarks[mp_hands.HandLandmark.WRIST].x and
            landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.WRIST].x):
            return "Come Here"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].x > landmarks[mp_hands.HandLandmark.WRIST].x and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].x > landmarks[mp_hands.HandLandmark.WRIST].x):
            return "Go There"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x and
            landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.WRIST].y):
            return "Eat"
        if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y and
            landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y):
            return "Drink"
        if (landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].y > landmarks[mp_hands.HandLandmark.PINKY_PIP].y):
            return "Fine"
        # "You" - Index finger pointing forward (other fingers down)
        if (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y and
            landmarks[mp_hands.HandLandmark.PINKY_TIP].y > landmarks[mp_hands.HandLandmark.PINKY_PIP].y):
            return "You"
        # "Are" - Index and Middle fingers up (V-shape), others down
        


        
    return None

def generate_frames():
    global sentence, last_gesture, last_detected_time

    cap = cv2.VideoCapture(0)
    gesture_history.clear()

    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize for faster processing
            small_frame = cv2.resize(frame_rgb, (320, 240))
            results = hands.process(small_frame)

            current_time = time.time()

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Scale landmarks back to original frame size
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    gesture = recognize_gesture(hand_landmarks)
                    if gesture:
                        gesture_history.append(gesture)

                        if gesture_history.count(gesture) >= 5 and gesture != last_gesture:
                            sentence += f"{gesture} "
                            last_gesture = gesture
                            last_detected_time = current_time

            # Display the latest gesture and sentence
            if gesture_history:
                recent = gesture_history[-1]
                cv2.putText(frame, f"Gesture: {recent}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if sentence.strip():
                cv2.putText(frame, f"Sentence: {sentence.strip()}", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

            # Reset sentence after 2 seconds of inactivity
            if current_time - last_detected_time > 2:
                sentence = ""
                last_gesture = ""

            # Efficient frame encoding
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/index', methods=['GET', 'POST'])
def shutdown():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
