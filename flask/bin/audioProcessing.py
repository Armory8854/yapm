from pydub import AudioSegment
#from tqdm import tqdm

#def progressBarBase(audio_file):
#    global progress_bar
#    step_size = 1000
#    total_steps = int(len(audio) / step_size)
#    progress_bar = tqdm(total=total_steps)
#    return progress_bar

def speedUpAudio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    print("Speeding up audio file...")
    fast_audio = audio.speedup(playback_speed=1.25, chunk_size=150)
    fast_audio.export(audio_file, format="mp3")

def trimAudio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    print("Removing Silence...")
    audio = audio.strip_silence()
    audio.export("test.mp3", format="mp3")
