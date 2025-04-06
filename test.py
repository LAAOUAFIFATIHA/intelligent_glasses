import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam.")
    exit()

# Load YOLO model
model_path = "C:/Users/hp/runs/detect/train222/weights/last.pt" # 22 30
model = YOLO(model_path)

threshold = 0.75  # Set threshold to 0.5  

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire la vidéo.")
        break

    # Display raw frame for debugging
    cv2.imshow("Raw Frame", frame)

    # Run inference
    results = model(frame)[0]  # Access the first element of the results list

    if "mark" in results:
        print("maaaaaaaaaaaaaaaaaaaark ")
        break

    # Process results
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        # Only display objects with a score > 0.50
        if score > threshold:
            print(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}, score: {score}, class_id: {class_id}")

            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

            # Format label with class name and probability
            label = f"{results.names[int(class_id)].upper()} {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Display the frame with detections
    cv2.imshow("YOLO Object Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
