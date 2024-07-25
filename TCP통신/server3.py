# server

import socket
import random

HOST = "127.0.0.1" # 호스트 지정
PORT = 5088 # 포트 번호 지정

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # 소켓 생성
    s.bind((HOST, PORT)) # 해당하는 포트에 연결하는 과정
    s.listen(5) # 해당하는 welcoming 소켓에 추가적으로 보내는 것이 있는지 없는지 듣는 것
    print("Guessing game server is ready")
    while True: 
        c, addr = s.accept() # TCP connection에 대한 소켓
    
        client_name = c.recv(1024).decode() # 클라이언트 이름을 받아오는 과정
        correct_answer = random.randint(1, 9) # 정답 숫자를 랜덤으로 받아오는 과정
        print(f'{client_name} is connected. The answer is {correct_answer}.')

        while True:
            received_data = c.recv(1024).decode() # 클라이언트로부터 데이터(숫자)를 받아옴
            received_number = int(received_data) # 데이터를 int형으로 변환
            print('Input : ', received_number)
            
            if received_number == 0: # 만약 입력받은 수가 0이라면
                c.sendall(b"Exit") # Exit 출력
                print(f'Exit game for {client_name}')
                break # 멈추기
            elif received_number > correct_answer: # 만약 입력받은 수가 정답보다 크다면
                c.sendall(b"Too high") # Too high 출력
            elif received_number < correct_answer: # 만약 입력받은 수가 정답보다 작다면
                c.sendall(b"Too low") # Too low 출력
            else: # 만약 입력받은 수가 정답이라면
                c.sendall(b"Correct") # Correct 출력
                print(f"Exit game for {client_name}.")
                break # 멈추기