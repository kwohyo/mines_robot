# client

import socket

HOST = "127.0.0.1" # 자기자신을 의미
PORT = 5088 # welcoming 포트

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # 소켓 생성
    s.connect((HOST, PORT)) # TCP connection을 만든다
    client_name = input("Input your name : ") # 이름 입력
    s.sendall(client_name.encode('utf-8')) # 이름을 인코딩해서 서버로 전송함

    print("Welcome! It's guessing game.")
        
    while True:
        n = input("Enter a number between 1-9 (Exit: 0) :")

        s.sendall(n.encode('utf-8')) # 숫자를 인코딩해서 서버로 전송함
        data = s.recv(1024).decode('utf-8') # response를 기다리는 부분
        print(f'Response : {data}') # 받은 데이터를 출력

        if data == 'Correct' or data == 'Exit': # data가 Correct나 Exit라면
            break # 멈추기