import cv2
from ultralytics import YOLO
import pyttsx3
import Cnn_firebase as fb
import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Load YOLO model
# model_path = "C:/Users/hp/runs/detect/train_4_50/weights/last.pt"
model_path = "C:/PFE1/train222/weights/last.pt"
model = YOLO(model_path)

threshold = 0.78  # Confidence threshold

# Variable to avoid repeating the alert too frequently
last_alert_time = 0
alert_cooldown = 3  ## time to wait 

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Run inference
    results = model(frame)[0]

    person_detected = False
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # print(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}, score: {score}, class_id: {class_id}")
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            label = f"{results.names[int(class_id)].upper()} {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            person_detected = True

            know_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

            local_path = f"images_Take/{results.names[int(class_id)]}{f'{know_date}'}.png"
            cloud_path = f"images/{results.names[int(class_id)]}{f'{know_date}'}.png"
            cv2.imwrite(local_path, frame)


            fb.add_To_dataBase(cloud_path , local_path , 
                               know_date,
                               results.names[int(class_id)] )

            # Speak "name" if an obj is found with cooldown
            if person_detected:
                current_time = cv2.getTickCount() / cv2.getTickFrequency()  # Get current time in seconds
                if current_time - last_alert_time > alert_cooldown:
                    engine.say(results.names[int(class_id)])
                    engine.runAndWait()  # Wait for speech to finish
                    last_alert_time = current_time  

    cv2.imshow("YOLO Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()