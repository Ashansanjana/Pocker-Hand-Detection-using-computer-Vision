# app.py
from flask import Flask, render_template, Response
import cv2
import cvzone
from ultralytics import YOLO
import math
# Assuming PokerHandFunction.py is in the same directory
import PokerHandFunction

# 1. Initialize Flask App
app = Flask(__name__)

# 2. Global Variables for Model and Classes
# IMPORTANT: Adjust the path to your model file!
model = YOLO("playingCards.pt") 

classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']

# 3. Video Capture and Frame Processing (Generator Function)
def generate_frames():
    # Use the same index as in your original code, may need to be 0 or -1
    cap = cv2.VideoCapture(0) 
    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        success, img = cap.read()
        if not success:
            break
        
        # --- Start of your original processing logic ---
        results = model(img, stream=True, verbose=False)
        hand = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), rt=0) # rt=0 for clean rect

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                
                # Draw class name and confidence
                card_name = classNames[cls]
                cvzone.putTextRect(img, f'{card_name} {conf}', 
                                   (max(0, x1), max(35, y1)), scale=1.5, thickness=2, offset=5)

                if conf > 0.5:
                    hand.append(card_name)
        
        # Determine the hand rank
        hand = list(set(hand))
        if len(hand) == 5:
            # We call the function from your separate file
            poker_result = PokerHandFunction.findPokerHand(hand)
            
            # Display the result in a large box
            cvzone.putTextRect(img, f'Hand: {poker_result}', (400, 70), 
                               scale=3, thickness=4, offset=15, colorR=(0, 255, 0))
        # --- End of your original processing logic ---
        
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Yield the frame in a format readable by the browser's <img> tag
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 4. Flask Routes
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Feeds the frame-by-frame MJPEG stream."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 5. Run the App
if __name__ == '__main__':
    # Use host='0.0.0.0' to make it accessible externally, e.g., for mobile testing
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)