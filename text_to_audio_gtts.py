from gtts import gTTS
import os

def text_to_speech_file(text,folder):
    
    audio_path = os.path.join(
        "user_uploads",folder,"audio.mp3"
    )

    tts = gTTS(
        text=text,lang="en",slow=False
    )
    tts.save(audio_path)

    return audio_path