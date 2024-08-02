from ultralytics import YOLO

# 훈련된 커스텀 yolo 모델을 불러오겠습니다.
#학습하여 모델이 만들어 질때마다 train1 처럼 폴더의 숫자가 커지며 그안에 best.pt이 생성됩니다.
#model = YOLO("../yolo8-face/runs/detect/train2/weights/best.pt") 
model = YOLO("C:\\MINESLAB\\yolov8-face\\runs\\detect\\train2\\weights\\best.pt")


# source에 test사진의 위치를 넣어주세요
model.predict(source="C:\\MINESLAB\\yolov8-face\\pill2.jpg", save=True, show=True)
# model.predict(source="C:\\MINESLAB\\yolov8-face\\pills.jpeg", save=True, show=True)