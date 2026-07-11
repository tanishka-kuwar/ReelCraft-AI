from flask import render_template, request, redirect, jsonify
from app import app

import os
import uuid

from upload_service import save_images, save_audio
from audio_service import text_to_speech_file
from reel_service import create_reel
from ai_service import (
    generate_script,
    generate_script_from_images,
    generate_hashtags_from_images,
    recommend_music
)
from audio_mixer import mix_audio

print("RUNNING ROUTES.PY")

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create", methods=["GET", "POST"])
def create():

    myid = str(uuid.uuid1())

    if request.method == "POST":

        rec_id = request.form.get("uuid")

        if not rec_id:
            rec_id = str(uuid.uuid4())

        print(request.form)
        desc = request.form.get("text") or ""
        print("TEXTAREA VALUE:")
        print(repr(desc))
        audio_type = request.form.get("audio_type")
        music_type = request.form.get("music_type")
        selected_music = request.form.get("selected_music")
        music_volume = int(request.form.get("music_volume", 25))
        
        reel_name = request.form.get("reel_name")

        if not reel_name:
            reel_name = "my_reel"

        folder_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            rec_id
        )

        os.makedirs(folder_path, exist_ok=True)

        # Save Images
        input_files = save_images(
            request,
            folder_path
        )

        durations = []

        for i in range(len(input_files)):

            d = request.form.get(f"duration{i+1}")

            durations.append(int(d))

        print("DESC =", desc)
        print("INPUT FILES =", input_files)
        print("DURATION =", durations)

        # Save description
        with open(
            os.path.join(folder_path, "desc.txt"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(desc)

        # Audio
        if audio_type == "upload":

            success = save_audio(
                request,
                folder_path
            )

            if not success:
                return "Please upload an audio file.", 400

        elif audio_type == "tts":

            if not desc:
                return "Please enter text.", 400

            text_to_speech_file(
                desc,
                rec_id
            )

        else:
            return "Invalid audio type.", 400
        
       # -------------------------
        # Voice Audio
        # -------------------------

        voice_audio = os.path.join(folder_path, "audio.mp3")

        music_audio = None

        # -------------------------
        # Manual Music
        # -------------------------

        if music_type == "manual":

            music_audio = os.path.join(
                "static",
                "music",
                f"{selected_music}.mp3"
            )

        # -------------------------
        # AI Recommended Music
        # -------------------------

        elif music_type == "ai":

            try:

                music_name = recommend_music(
                    folder_path,
                    input_files
                )

            except Exception as e:

                print("Gemini Error:", e)
                print("Using fallback music: chill")

                music_name = "chill"

            music_name = (
                music_name
                .strip()
                .lower()
                .replace(".", "")
                .replace(",", "")
            )

            allowed = {
                "chill",
                "travel",
                "happy",
                "cinematic",
                "emotional",
                "energetic"
            }

            if music_name not in allowed:

                print("Invalid category:", music_name)
                music_name = "chill"

            print("AI Recommended Music:", music_name)

            music_audio = os.path.join(
                "static",
                "music",
                f"{music_name}.mp3"
            )
        print("Music Type:", music_type)
        print("Selected Music:", selected_music)
        print("Music Audio Path:", music_audio)
        print("Exists:", os.path.exists(music_audio) if music_audio else False)

        # -------------------------
        # Mix Voice + Background Music
        # -------------------------

        if music_audio:

            if music_audio and os.path.exists(music_audio):

                print("Using music:", music_audio)

                final_audio = os.path.join(
                    folder_path,
                    "final_audio.mp3"
                )

                success = mix_audio(
                    voice_audio,
                    music_audio,
                    final_audio,
                    music_volume
                )

                if success:

                    if os.path.exists(voice_audio):
                        os.remove(voice_audio)

                    os.rename(
                        final_audio,
                        voice_audio
                    )

                # create reel
            success = create_reel(
            folder_path,
            rec_id,
            reel_name,
            desc,
            durations,
            input_files
            )

            if not success:
                return "Reel generation failed.", 500

            return redirect("/gallery")

    return render_template(
        "create.html",
        myid=myid
    )

@app.route("/generate-script", methods=["POST"])
def generate_ai_script():

    from werkzeug.utils import secure_filename
    import tempfile
    import os

    image_paths = []

    try:

        images = request.files.getlist("images")

        if len(images) == 0:
            return jsonify({"script": "Please upload images first."})

        temp_dir = tempfile.mkdtemp()

        for image in images:

            filename = secure_filename(image.filename)

            path = os.path.join(temp_dir, filename)

            image.save(path)

            image_paths.append(path)

        script = generate_script_from_images(image_paths)

        return jsonify({
            "script": script
        })

    except Exception as e:

        print(e)

        return jsonify({
            "script": str(e)
        }), 500

    finally:

        for path in image_paths:

            if os.path.exists(path):
                os.remove(path)

        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)

@app.route("/gallery")
def gallery():

    reels_dir = os.path.join(
        "static",
        "reels"
    )

    os.makedirs(
        reels_dir,
        exist_ok=True
    )

    reels = os.listdir(reels_dir)

    return render_template(
        "gallery.html",
        reels=reels
    )


@app.route("/delete/<reel>")
def delete_reel(reel):

    reel_path = os.path.join(
        "static",
        "reels",
        reel
    )

    if os.path.exists(reel_path):
        os.remove(reel_path)

    return redirect("/gallery")

@app.route("/generate-hashtags", methods=["POST"])
def generate_ai_hashtags():

    from werkzeug.utils import secure_filename
    import tempfile
    import os

    image_paths = []

    try:

        images = request.files.getlist("images")

        if len(images) == 0:
            return jsonify({
                "hashtags": "Please upload images first."
            })

        temp_dir = tempfile.mkdtemp()

        for image in images:

            filename = secure_filename(image.filename)

            path = os.path.join(temp_dir, filename)

            image.save(path)

            image_paths.append(path)

        hashtags = generate_hashtags_from_images(image_paths)

        return jsonify({
            "hashtags": hashtags
        })

    except Exception as e:

        print(e)

        return jsonify({
            "hashtags": str(e)
        }), 500

    finally:

        for path in image_paths:
            if os.path.exists(path):
                os.remove(path)

        if 'temp_dir' in locals():
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
