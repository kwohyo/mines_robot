import socket
import sounddevice as sd
import numpy as np

SERVER_IP = '서버 IP 주소'  # 실제 IP 주소로 변경 필요
PORT = 12345  # 유효한 포트 번호로 변경 필요

def record_audio(duration, fs=16000):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio

def play_audio(fs, audio):
    sd.play(audio, samplerate=fs)
    sd.wait()

def main():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, PORT))
                print("Connected to server.")

                while True:
                    input("Press Enter to start recording, then press Enter again to stop.")
                    
                    # 음성 데이터 녹음
                    duration = 5  # 녹음 시간 (초)
                    audio_data = record_audio(duration)
                    
                    # 서버로 음성 데이터 전송
                    s.sendall(audio_data.tobytes())
                    
                    # 서버로부터 LLM 응답 수신
                    response_data = b''
                    while True:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        response_data += chunk
                    
                    if not response_data:
                        print("No response received from the server.")
                        continue
                    
                    # 응답 데이터를 float32로 변환
                    response_audio = np.frombuffer(response_data, dtype='float32')
                    
                    # 음성 데이터 재생
                    play_audio(16000, response_audio)
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
