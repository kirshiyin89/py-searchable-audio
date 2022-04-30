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
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    audio_text = ""

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"{file_name}{i}")
        audio_chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_file = speech_recognizer.record(source)
            try:
                text = speech_recognizer.recognize_google(audio_file)

            except sr.UnknownValueError as e:
                print("An Error has occurred while recognising audio file:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                audio_text += text
                
                os.remove(chunk_filename)
                
    return audio_text

def find_keyword(keyword):
   	for f in os.scandir("/home/kirshi/py-searchable-audio/texts"):
   	    print("searching in f" + str(f))
   	    file_content = open(f).read()
   	    text_tokens = tokenizer.tokenize(file_content)
   	    word_count = len(text_tokens)
   	    print(word_count)
   	    file_content.index(keyword)
   	    res = re.sub("[^\w]", " ",  file_content).split()
   	    res = res.index(keyword) + 1
   	    print(res)
   	    text = Text(text_tokens)
   	    print(text.concordance(keyword))
               

if __name__ == '__main__':

	keyword = input("Enter your search keyword: ")
	
	for file_name in os.scandir("/home/kirshi/py-searchable-audio"):
		ext = os.path.splitext(file_name)[-1].lower()
		file_path = f"texts/{os.path.basename(file_name).split('.')[0] }" + ".txt"
		if file_name.is_file and ext.endswith(".wav") and not os.path.exists(file_path):
			fh = open(file_path, "w+")
			fh.write(transcribe_audio(file_name))
			fh.close()
			
	find_keyword(keyword)
					

                           		
