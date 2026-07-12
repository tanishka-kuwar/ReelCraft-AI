import os
import re
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = { "jpg",
                            "jpeg",
                            "png",
                            "jfif",
                            "bmp",
                            "gif",
                            "webp",
                            "tiff",
                            "tif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def save_images(request, folder_path):

    input_files = []

    for key in request.files:

        if not key.startswith("file"):
            continue

        file = request.files[key]

        if file.filename == "":
            continue

        # Clean filename
        name = os.path.splitext(file.filename)[0]
        name = re.sub(r'[^A-Za-z0-9_-]', "_", name)

        filename = f"{name}.jpg"

        path = os.path.join(folder_path, filename)

        img = Image.open(file)

        # Convert images with transparency correctly
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        else:
            img = img.convert("RGB")

        img.thumbnail((1920, 1920))
        img.save(path, "JPEG", quality=95)

        input_files.append(filename)

    return input_files

def save_audio(request, folder_path):

    audio = request.files.get("audio_file")

    if audio and audio.filename:

        audio.save(
            os.path.join(folder_path, "audio.mp3")
        )

        return True

    return False