#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class server:
    def __init__(self,host='',port=12345):
        self.host = host
        self.port = port
        self.stt = whisper.load_model('base.en')
        self.tts = TextToSpeeckService()
        self.template = '''
        You are a helpful and friendly AI assistant. You are polite, respectful, and aim to provide clear and concise instructions for performing actions.
        The conversation transcript is as follows:{history}
        And here is the user's follow-up: {input}
        Your response:

        1. Clearly state the action the user should perform.
        2. Provide a step-by-step guide to perform the action.
        3. Offer additional tips or suggestions for successful completion.

        Response:
        '''
        self.prompt = PromptTemplate(input_variables=['history','input'],template=self.template)
        self.chain = ConversationChain(
            prompt = self.prompt,
            verbos = False,
            memory = ConversationBufferMemory(ai_prefix = 'Assistant:'),
            llm = Ollama(models='llama3')
        )
        

    def handle_client(self, conn, addr):
        try:
            print('로봇과 연결')
            
            audio_data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                audio_data += chunk
                
            print('파일 전송 받음')
            audio_np = np.frombuffer(audio_data, dtype = np.int16).astype(np.float32)/32768.0
            
            text = self.stt.transcribe(audio_np)['text']
            print(f"음성을 텍스트로 바꾼 결과:{text}")
            
            response = self.chain.predict(input=text)
            print(f"LLM결과 : {response}")
            
            sample_rate, response_audio = self.tts.long_from_synthesize(response)
            
            response_filename = 'response_output.wav'
            wav.write(response_filename, sample_rate, (response_audio*32767).astype(np.int16))
            print("wav파일로 LLM결과 저장완료")
            
            #응답파일전송
            with open(response_filename, 'rb') as file:
                while chunk := file.read(4096):
                        conn.sendall(chunk)
                        
            print('응답결과를 로봇에 전달')
            
        except Exception as e:
            print(f"Error handling client {addr}:{e}")
            
        finally:
            conn.close()
            print(f'connection with {addr} closed')
            
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn.addr))
                client_thread.start()
                
if __name__ == '__main__':
    server = Server()
    server.run()

