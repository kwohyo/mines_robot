import socket
import threading
import numpy as np
import whisper
from queue import Queue
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from tts import TextToSpeechService

#model(text<->speech)
stt = whisper.load_model("base.en") #speech->text
tts = TextToSpeechService() #text->speech

# LangChain 설정
template = """
You are a helpful and friendly AI assistant. You are polite, respectful, and aim to provide clear and concise instructions for performing actions.
The conversation transcript is as follows:
{history}
And here is the user's follow-up: {input}
Your response:

1. Clearly state the action the user should perform.
2. Provide a step-by-step guide to perform the action.
3. Offer additional tips or suggestions for successful completion.

Response:
"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
chain = ConversationChain(
    prompt=PROMPT,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="Assistant:"),
    llm=Ollama(model = "llama3"),
)

def handle_client(conn, addr):
    try:
        # 데이터 수신
        print('please send me audio data')
        audio_data = conn.recv(4096)
        print('audio_data :', audio_data)
        # audio_data = b''
        # while True:
        #     chunk = conn.recv(4096)
        #     if not chunk:
        #         break
        #     audio_data += chunk
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        print('audio_np :', audio_np)
        print('audio_np shape :', audio_np.shape)

        
        # STT 수행
        text = stt.transcribe(audio_np)["text"]
        print(f"Transcribed text: {text}")
        
        # LLM 응답 생성
        response = chain.predict(input=text)
        print(f"LLM Response: {response}")
        
        # TTS 수행
        sample_rate, response_audio = tts.long_form_synthesize(response)
        # data = str(sample_rate) + ',' + np.array2string(response_audio)
        print('sample_rate dtype :', type(sample_rate))
        print('response_audio dtype :', response_audio.dtype)
        
        # 응답 전송
        conn.sendall(response_audio.tobytes())
        print('sent speak')
    finally:
        conn.close()

def main():
    HOST = '192.168.0.55'  # 서버가 모든 인터페이스에서 수신 대기
    PORT = 12345 # 포트 번호

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening on port", PORT)
        conn, addr = s.accept()
        print('connected to client!')

        while True:
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
