# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np

## TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
s.connect(('127.0.0.1', 8485))

## webcam 이미지 capture
cam = cv2.VideoCapture(0)

## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 320)
cam.set(4, 240)

## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # 비디오의 한 프레임씩 읽는다.
    ret, frame = cam.read()
    if not ret:
        break
    
    # 프레임을 JPEG로 인코딩
    result, frame_encoded = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(frame_encoded)
    stringData = data.tobytes()

    # 서버에 데이터 전송
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    
    # 서버로부터 객체 이름 수신
    objects_data = s.recv(64)  # 최대 64바이트까지 수신
    objects_str = objects_data.decode().strip()
    detected_objects = objects_str.split(',')

    # 수신한 객체의 이름을 출력
    for obj in detected_objects:
        if obj:
            print(f"Detected object from server: {obj}")

    # 비디오 프레임을 화면에 표시
    cv2.imshow('Client Sending Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
s.close()
