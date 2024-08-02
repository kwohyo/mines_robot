# DOA.py, VAD.py 라이브러리
from tuning import Tuning
import usb.core
import usb.util
import time

# record.py 라이브러리
import pyaudio
import wave
import numpy as np



class ReSpeaker_Mic_Array_v2():
    '''
    ReSpeaker Mic Array v2.0 마이크의 기능을 모아둔 클래스
    '''

    def __init__(self):
        self.RESPEAKER_RATE = 16000
        self.RESPEAKER_CHANNELS = 6
        self.RESPEAKER_WIDTH = 2
        self.CHUNK = 1024
        self.RECORD_SECONDS = 3 # 녹음 시간(초)
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.RESPEAKER_INDEX = self.getDeviceInfo()
        self.VENDER_ID = 0x2886
        self.PRODUCT_ID = 0x0018


    def getDeviceInfo(self):
        '''
        마이크의 device ID 정보를 반환하는 함수
        '''

        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i) # i번째 device의 정보
            if (device_info.get('maxInputChannels')) > 0:
                if device_info.get('name') == 'ReSpeaker 4 Mic Array (UAC1.0): USB Audio (hw:1,0)': # 마이크의 device ID 찾기
                    print("Input Device id ", i, " - ", device_info.get('name'))
                    device_ID = i

        try:
            return device_ID
        except:
            print('[Error] Device ID was not detected.')
    

    def doa(self):
        '''
        DOA(Direction of Arrival)를 반환하는 함수
        DOA란? : 마이크에 외부 소리가 도달하는 각도
        '''

        dev = usb.core.find(idVendor = self.VENDER_ID, idProduct = self.PRODUCT_ID)

        if dev:
            Mic_tuning = Tuning(dev)
            DOA = Mic_tuning.direction
            print('DOA(Direction of Arrival):', DOA)

        try:
            return DOA
        except:
            print('[Error] DOA was not detected.')
        

    def vad(self):
        '''
        VAD(Voice Activity Detection)를 반환하는 함수
        VAD란? : 마이크에서 사람의 목소리가 감지되는지 여부
        '''
        
        dev = usb.core.find(idVendor = self.VENDER_ID, idProduct = self.PRODUCT_ID)

        if dev:
            Mic_tuning = Tuning(dev)
            VAD = Mic_tuning.is_voice()
            print('VAD(Voice Activity Detection):', VAD)

        try:
            return VAD
        except:
            print('[Error] VAD was not detected.')


    def record(self):
        '''
        마이크로 소리를 녹음하는 함수
        '''

        p = pyaudio.PyAudio()

        stream = p.open(
                    rate = self.RESPEAKER_RATE,
                    format = p.get_format_from_width(self.RESPEAKER_WIDTH),
                    channels = self.RESPEAKER_CHANNELS,
                    input = True,
                    input_device_index = self.RESPEAKER_INDEX,)

        print("*** Recording...")

        # Recording
        '''frames = []
        no_voice_activity = 0
        while True:
            # 1초 동안 녹음
            for i in range(0, int(self.RESPEAKER_RATE / self.CHUNK)):
                data = stream.read(self.CHUNK)
                a = np.fromstring(data, dtype = np.int16)[0::6]
                frames.append(a.tostring())

            # 3초 동안 사람의 목소리가 감지되지 않으면 녹음 중단
            if no_voice:
                break'''



        frames = [] 
        for i in range(0, int(self.RESPEAKER_RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            # extract channel 0 data from 6 channels, if you want to extract channel 1, please change to [1::6]
            a = np.fromstring(data, dtype = np.int16)[0::6]
            frames.append(a.tostring())

        print("*** Done recording.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(p.get_format_from_width(self.RESPEAKER_WIDTH)))
        wf.setframerate(self.RESPEAKER_RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        

if __name__ == '__main__':
    mic = ReSpeaker_Mic_Array_v2()
    # check DOA
    DOA = mic.doa()

    # check VAD
    VAD = mic.vad()

    # extract voice
    mic.record()

