import socket
import cv2
import numpy as np
from threading import Thread
from ultralytics import YOLO

# socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def run_server_and_yolo():
    model = YOLO('yolov8n.pt')
    
    HOST = '192.168.0.74'  # 서버 IP
    PORT = 8485

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST, PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn, addr = s.accept()

    while True:
        length = recvall(conn, 16)
        if not length:
            break
        stringData = recvall(conn, int(length))
        if not stringData:
            break
        data = np.frombuffer(stringData, dtype='uint8')

        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        
        # YOLO 모델을 사용하여 객체 검출
        results = model(frame)
        annotated_frame = results[0].plot()

        # 객체의 이름 추출
        detected_objects = []
        for result in results[0].boxes:
            class_id = int(result.cls[0])
            class_name = model.names[class_id]
            detected_objects.append(class_name)
            print(f"Detected object: {class_name}")

        # 객체의 이름을 클라이언트로 전송
        objects_str = ','.join(detected_objects)
        conn.sendall(objects_str.encode().ljust(64))  # 최대 64바이트까지 패딩
        
        cv2.imshow('YOLOv8 Inference', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    conn.close()
    s.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    server_yolo_thread = Thread(target=run_server_and_yolo)
    server_yolo_thread.start()
    server_yolo_thread.join()
