import time
import threading
import numpy as np
import whisper
import sounddevice as sd
from queue import Queue
from rich.console import Console
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from tts import TextToSpeechService
import os
from scipy.io import wavfile

console = Console()
stt = whisper.load_model("base.en")
tts = TextToSpeechService()

template = """
You are polite, respectful, and aim to provide concise responses of less 
than 20 words.

And here is the user's follow-up: {input}

Your response:

1. Provide a step-by-step guide to perform the action.
2. Offer additional tips or suggestions for successful completion.
"""

PROMPT = PromptTemplate(input_variables=["input"], template=template)
chain = ConversationChain(
    prompt=PROMPT,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="Assistant:"),
    llm=Ollama(model='llama3'),
)

def transcribe(audio_np: np.ndarray) -> str:

    result = stt.transcribe(audio_np, fp16=False)  # Set fp16=True if using a GPU
    text = result["text"].strip()
    return text


def get_llm_response(text: str) -> str:

    response = chain.predict(input=text)
    if response.startswith("Assistant:"):
        response = response[len("Assistant:") :].strip()
    return response

def save_audio_to_wav(sample_rate, audio_array, filename):
    wavfile.write(filename, sample_rate, audio_array)
    console.print(f"[green]Audio saved to {filename}")


if __name__ == "__main__":
    console.print("[cyan]Assistant started! Press Ctrl+C to exit.")

    try:
        audio_file_path = '/home/ubuntu/Desktop/mines_lab/mines_robot/chat/output.wav'
        if os.path.exits(audio_file_path):
            sample_rate, audio_np = wavfile.read(audio_file_path)
            audio_np = audio_np.astype(np.float32)/32768.0

            if audio_np.size > 0:
                with console.status('Transcribing...',spinner='earth'):
                    text = transcribe(audio_np)
                console.print(f"[yellow]You : {text}")

                with console.status('Generating response...',spinner='earth'):
                    response = get_llm_response(text)
                    sample_rate, audio_array = tts.long_form_synthesize(response)

                output_wav_path = '/home/ubuntu/Desktop/mines_lab/mines_robot/chat/response.wav'
                save_audio_to_wav(sample_rate,audio_array,output_wav_path)
            else:
                console.print('[red]No audio data found in the file.')

        else:
            console.print(f"[red]Audio file not found at file_path")

    except KeyboardInterrupt:
        console.print('\n[red]Finish')

    console.print("[blue]Session END")