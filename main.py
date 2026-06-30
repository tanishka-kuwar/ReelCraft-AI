from flask import Flask, render_template, request, redirect
# Generate unique folder IDs for each reel
import uuid
import os
#  to upload any file
# secure_filename makes file names safe for OS and FFmpeg
from werkzeug.utils import secure_filename

from text_to_audio_gtts import text_to_speech_file

import subprocess

def create_reel(folder, reel_name,caption_text):

    input_txt = f"user_uploads/{folder}/input.txt"
    audio_mp3 = f"user_uploads/{folder}/audio.mp3"
    output_mp4 = f"static/reels/{reel_name}_{folder[:8]}.mp4"
    caption_text = caption_text.replace("'","\\'")
    font_path = "C\\:/Windows/Fonts/arial.ttf"

    os.makedirs("static/reels", exist_ok=True)

    command = (
    f'ffmpeg -y -f concat -safe 0 '
    f'-i "{input_txt}" '
    f'-i "{audio_mp3}" '
    f'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
    f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,'
    # f'drawtext=fontfile={font_path}:'
    f'drawtext=text=\'{caption_text}\':'
    f'fontcolor=white:'
    f'fontsize=48:'
    f'box=1:'
    f'boxcolor=black@0.5:'
    f'boxborderw=10:'
    f'x=(w-text_w)/2:'
    f'y=h-150" '

    f'-c:v libx264 -c:a aac -shortest '
    f'-r 30 -pix_fmt yuv420p '
    f'"{output_mp4}"'

)

    print("Starting FFmpeg...")
    subprocess.run(command, shell=True, check=True)
    print("FFmpeg Finished!")

UPLOAD_FOLDER = 'user_uploads' #name of folder where we want to save input files
ALLOWED_EXTENSION = {'png','jpg','jpeg'}

def allowed_file(filename):
    return("." in filename and
            filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSION
            )

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/")

def home():

    return render_template("home.html")

@app.route("/create", methods=["GET","POST"])

def create():

    # unique id for each reel
    myid = str(uuid.uuid1())

    if request.method == "POST":
        rec_id = request.form.get("uuid")
        if not rec_id:
            rec_id = str(uuid.uuid4())
        desc = request.form.get("text") or ""
        audio_type = request.form.get("audio_type")
        duration = request.form.get("duration")
        reel_name = request.form.get("reel_name")

        reel_name = request.form.get("reel_name")
        print("FROM DATA: ",request.form)
        print("UUID:",request.form.get("uuid"))
        print("FORM:", request.form)
        print("FILES:", request.files)
        print("CONTENT TYPE:", request.content_type)

        if not reel_name:
            reel_name = "my_reel"
        
        reel_name = secure_filename(reel_name)

        folder_path = os.path.join(
            app.config["UPLOAD_FOLDER"],rec_id
        )

        os.makedirs(folder_path,exist_ok=True) 

        input_files = []

        # Save uploaded images to user-specific folder
        for key,file in request.files.items():
            if key == "audio_file":
                continue
            if file and file.filename:
                if not allowed_file(file.filename):
                    continue
                filename = secure_filename(file.filename)
                file.save(os.path.join(folder_path, filename))
                input_files.append(filename)

        # save desc.txt
        with open(
            os.path.join(folder_path,"desc.txt"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(desc)

        # Generate FFmpeg slideshow configuration
        input_txt_path = os.path.join(folder_path, "input.txt")
        
        with open(input_txt_path,"w") as f:
            for f1 in input_files:
                img_path = os.path.abspath(os.path.join(folder_path, f1))

                f.write(f"file '{img_path}' \n")
                f.write(f"duration {duration} \n")

            if input_files:
                last_img = os.path.abspath(
                    os.path.join(folder_path,input_files[-1])
                )
                f.write(f"file '{last_img}' \n")

        # handle audio upload
        if audio_type == "upload":
            audio = request.files.get("audio_file")

            if audio and audio.filename:
                audio.save(
                    os.path.join(folder_path, "audio.mp3")
                )

        # Generate narration using gTTS
        else:
            text_to_speech_file(desc,rec_id) # this creates audio.mp3 automatically

        print("INPUT FILES:",input_files)
        print("AUDIO TYPE:", audio_type)
        # Create final reel using FFmpeg
        create_reel(rec_id , reel_name, desc)
        print("REEL CREATED SUCCESSFULLY")

        return redirect("/gallery")

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():

    print("GALLERY OPENED")

    reels_dir = os.path.join("static","reels")

    if not os.path.exists(reels_dir):
        os.makedirs(reels_dir)

    reels = os.listdir(reels_dir)

    print("REELS:", reels)

    return render_template("gallery.html", reels=reels)

@app.route("/delete/<reel>")

def delete_reel(reel):

    reel_path = os.path.join("static", "reels", reel)

    if os.path.exists(reel_path):
        os.remove(reel_path)

    return redirect("/gallery")
    
if __name__ == "__main__":
    app.run(debug=True)