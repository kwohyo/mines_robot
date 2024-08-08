import cv2
from ultralytics import YOLO

model = YOLO('C:/MINESLAB/yolov8-face/runs/detect/train2/weights/best.pt') # best.pt의 경로

cap=cv2.VideoCapture(0)

while cap.isOpened():
    success, frame=cap.read()

    if success:
        results=model(frame)
        annotated_frame=results[0].plot()
        cv2.imshow("YOLOv8 Inference",annotated_frame)

        if cv2.waitKey(1) & 0xFF==ord("q"):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
