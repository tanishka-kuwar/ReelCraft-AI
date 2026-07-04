from gtts import gTTS
import os


def text_to_speech_file(text, rec_id):

    folder_path = os.path.join("user_uploads", rec_id)

    os.makedirs(folder_path, exist_ok=True)

    output_file = os.path.join(folder_path, "audio.mp3")

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save(output_file)

    return output_file