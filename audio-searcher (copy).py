# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()
# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    file_name = os.path.basename(path) 

    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"{file_name}{i}")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)

            except sr.UnknownValueError as e:
                print("Error:", e)
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

                os.remove(chunk_filename)
    # return the text for all chunks detected
    return whole_text

def find_keyword(keyword):
    for f in os.scandir("/home/dwp3410/projects/py-audio"):
        ext = os.path.splitext(f)[-1].lower()
        if f.is_file and ext.endswith(".txt"):
            print(f"searching in f{str(f)}")
            with open(f, 'r') as infile:
                for line in infile:
                    if keyword in line:
                        print(f"keyword matched in file {str(f)}")
               

if __name__ == '__main__':

    keyword = input("Enter your search keyword: ")

    for file_name in os.scandir("/home/dwp3410/projects/py-audio"):
        ext = os.path.splitext(file_name)[-1].lower()
        print(f"filename: {str(file_name)}")
        if (
            file_name.is_file
            and ext.endswith(".wav")
            and not os.path.exists(f"{os.path.basename(file_name)}.txt")
        ):
            with open(f"{os.path.basename(file_name)}.txt", "w+") as fh:
                fh.write((get_large_audio_transcription(file_name)))
    find_keyword(keyword)		

                           		
