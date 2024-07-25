import socket
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

SERVER_IP = '192.168.0.55'
PORT = 12345  # 서버 포트 번호-TCP(12345)

def record_audio(duration, fs=16000):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    print("Waiting End Recording audio...")
    sd.wait()
    return audio

def play_audio(fs, audio):
    print('Playing received LLM response...')
    sd.play(audio, samplerate=fs)
    print('Waiting End Playing received LLM response...')
    sd.wait()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))

        while True:
            input("Press Enter to start recording, then press Enter again to stop.")
            
            # 음성 데이터 녹음
            duration = 5  # 녹음 시간 (초)
            audio_data = record_audio(duration)
            print('audio_data :', audio_data)
            print('audio_data shape :', audio_data.shape)
            print('recorded audio')
            
            # 서버로 음성 데이터 전송
            s.sendall(audio_data.tobytes())
            print('sent audio')
                
            # 서버로부터 LLM 응답 수신
            response_data = s.recv(4096)
            # response_data = b''
            # while True:
            #     chunk = s.recv(4096)
            #     if not chunk:
            #         break
            #     response_data += chunk
            print('received LLM response')
            response_audio = np.frombuffer(response_data, dtype=np.float32)
            # data = data.decode()
            # sample_rate = data.split(',')[0]
            # response_audio = data.split(',')[1]
            print('received LLM response :', response_audio)
            
            # 음성 데이터 재생
            play_audio(16000, response_audio)
            print('played received LLM response')

            wav.write('output.wav', 16000, (response_audio * 32767).astype(np.int16))

if __name__ == "__main__":
    main()
