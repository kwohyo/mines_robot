import socket
import wave
from MIC.microphone import ReSpeaker_Mic_Array_v2


class ChatBot:
    def __init__(self):
        self.HOST = '192.168.0.55'
        self.PORT = 1234
        self.socket = self.connect_to_server()
        self.mic = self.prepare_microphone()
        self.output_wav_filename = 'output.wav' # 음성 녹음한 결과 wav 파일


    def connect_to_server(self):
        '''
        서버와 연결하는 함수
        '''

        print('Connecting to server...')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        print('Connected to server!')

        return s


    def close_connection_with_server(self):
        '''
        서버와의 연결을 닫는 함수
        '''

        self.socket.close()
        print('Closed connection with server.')


    def stop_chatbot(self):
        '''
        챗봇을 중지시키는 함수
        '''
        self.close_connection_with_server()
        print('Stopped chatbot.')


    def prepare_microphone(self):
        '''
        마이크를 사용할 준비를 하는 함수
        '''

        mic = ReSpeaker_Mic_Array_v2()
        print("Chatbot's microphone is ready.")

        return mic


    def listen_to_human(self):
        '''
        사람의 음성을 녹음하는 함수
        '''

        self.mic.record(self.output_wav_filename)


    def send_to_server(self):
        '''
        서버에게 녹음된 wav 파일을 송신하는 함수
        '''

        f = wave.open(self.output_wav_filename, 'rb')
        data = self.mic.read_frames(f)

        self.socket.send(data)
        print('Sent the recorded WAV file to server.')


    def receive_from_server(self):
        '''
        서버로부터 wav 파일을 수신하는 함수
        '''

        data = []
        while True:
            d = self.socket.recv(self.mic.CHUNK)
            if not d:
                break
            data.append(d)
        data = b''.join(data)

        print('Received the generated WAV file from server.')

        return data
    

    def speak_to_human(self):
        '''
        서버로부터 수신한 wav 파일을 재생하는 함수
        '''

        data = self.receive_from_server() # 재생하고 싶은 wav 파일
        self.mic._play(data)



if __name__ == '__main__':

    chatbot = ChatBot()

    chatbot.listen_to_human()
    chatbot.send_to_server()
    chatbot.receive_from_server()
    chatbot.speak_to_human()

    chatbot.stop_chatbot()
