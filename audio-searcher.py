import speech_recognition as sr 
import os 
import re
import nltk
from pydub import AudioSegment
from pydub.silence import split_on_silence
from nltk.tokenize import RegexpTokenizer
from nltk.text import Text


speech_recognizer = sr.Recognizer()
tokenizer = RegexpTokenizer(r'\w+')

def transcribe_audio(path):

    audio = AudioSegment.from_wav(path)
    file_name = os.path.basename(path) 

    chunks = split_on_silence(audio,
        min_silence_len = 600,
        silence_thresh = audio.dBFS-14,
        keep_silence=600,
    )
    audio_folder = "audio-chunks"
    if not os.path.isdir(audio_folder):
        os.mkdir(audio_folder)

    audio_text = ""

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(audio_folder, f"{file_name}{i}")
        audio_chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_file = speech_recognizer.record(source)
            try:
                text = speech_recognizer.recognize_google(audio_file)

            except sr.UnknownValueError as e:
                print("An error has occurred while recognising audio file:", e)
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                audio_text += text

                os.remove(chunk_filename)

    return audio_text

def find_keyword(keyword):
    for f in os.scandir("/home/kirshi/py-searchable-audio/texts"):
        print(f"searching in f{str(f)}")
        file_content = open(f).read()
        text_tokens = tokenizer.tokenize(file_content)
        text = Text(text_tokens)
        print(text.concordance(keyword))
 
   	       
def start_search(keyword):
    for file_name in os.scandir("/home/kirshi/py-searchable-audio"):
        extension = os.path.splitext(file_name)[-1].lower()
        file_path = f"texts/{os.path.basename(file_name).split('.')[0]}.txt"
        if file_name.is_file and extension.endswith(".wav") and not os.path.exists(file_path):
            with open(file_path, "w+") as fh:
                fh.write(transcribe_audio(file_name))
    find_keyword(keyword)		              

if __name__ == '__main__':

	keyword = input("Enter a search keyword: ")
	
	start_search(keyword)
			
	
					

                           		
