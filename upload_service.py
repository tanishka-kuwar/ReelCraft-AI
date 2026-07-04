import os
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "jfif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def save_images(request, folder_path):

    input_files = []

    print("FILES RECEIVED:", request.files)

    for key in request.files:

        print("KEY:", key)

        file = request.files[key]

        print("FILENAME:", file.filename)

        if key == "audio_file":
            continue

        if file and file.filename:

            if not allowed_file(file.filename):
                print(f"Skipped: {file.filename}")
                continue

            filename = secure_filename(file.filename)

            file.save(os.path.join(folder_path, filename))

            input_files.append(filename)

    print("FINAL INPUT FILES:", input_files)

    return input_files

def save_audio(request, folder_path):

    audio = request.files.get("audio_file")

    if audio and audio.filename:

        audio.save(
            os.path.join(folder_path, "audio.mp3")
        )

        return True

    return False