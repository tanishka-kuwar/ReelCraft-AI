import os
import subprocess

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp",
    ".tif",
    ".tiff"
}

def run(cmd):

    print("=" * 100)
    print(cmd)
    print("=" * 100)

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    print("Return Code:", result.returncode)

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    return result.returncode == 0


def create_reel(
    folder_path,
    rec_id,
    reel_name,
    caption_text,
    durations,
    input_files,
    transition
):

    os.makedirs("static/reels", exist_ok=True)

    temp_videos = []

    # ------------------------
    # Step 1
    # Create one video per image
    # ------------------------

    for i, media in enumerate(input_files):

        media_path = os.path.abspath(
            os.path.join(folder_path, media)
        ).replace("\\", "/")

        temp_video = os.path.join(
            folder_path,
            f"temp_{i}.mp4"
        )

        temp_videos.append(temp_video)

        extension = os.path.splitext(media)[1].lower()

        # ---------------- IMAGE ----------------
        if extension in IMAGE_EXTENSIONS:

            cmd = (
                f'ffmpeg -y '
                f'-loop 1 '
                f'-i "{media_path}" '
                f'-t {durations[i]} '
                f'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
                f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
                f'-r 30 '
                f'-pix_fmt yuv420p '
                f'-c:v libx264 '
                f'"{temp_video}"'
            )

        # ---------------- VIDEO ----------------
        else:
            print("=" * 50)
            print("VIDEO:", media)
            print("Selected Duration:", durations[i])
            print("=" * 50)
            cmd = (
                f'ffmpeg -y '
                f'-i "{media_path}" '
                f'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
                f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
                f'-r 30 '
                f'-pix_fmt yuv420p '
                f'-c:v libx264 '
                f'-c:a aac '
                f'"{temp_video}"'
            )

        if not run(cmd):
            return False

    # ------------------------
    # Step 2
    # Make videos.txt
    # ------------------------

    videos_txt = os.path.join(
        folder_path,
        "videos.txt"
    )

    with open(videos_txt, "w") as f:

        for video in temp_videos:

            absolute = os.path.abspath(video).replace("\\", "/")

            f.write(f"file '{absolute}'\n")
    # ------------------------
    # Step 3
    # Join videos
    # ------------------------

    slideshow = os.path.join(
        folder_path,
        "slideshow.mp4"
    )

    cmd = (
        f'ffmpeg -y '
        f'-f concat '
        f'-safe 0 '
        f'-i "{videos_txt}" '
        f'-c copy '
        f'"{slideshow}"'
    )

    if not run(cmd):
        return False

    # ------------------------
    # Step 4
    # Add audio + caption
    # ------------------------

    audio = os.path.join(
        folder_path,
        "audio.mp3"
    )

    has_audio = os.path.exists(audio)

    print("Has Audio:", has_audio)

    output = os.path.join(
        "static",
        "reels",
        f"{reel_name}_{rec_id[:8]}.mp4"
    )

    caption_text = (
        caption_text
        .replace("\r", " ")
        .replace("\n", " ")
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", r"\'")
        .replace('"', r'\"')
        .replace(",", r"\,")
        .replace("[", r"\[")
        .replace("]", r"\]")
        .strip()
    )
    caption_file = os.path.join(folder_path, "caption.txt")
    caption_file = caption_file.replace("\\", "/")

    with open(caption_file, "w", encoding="utf-8") as f:
        f.write(caption_text)

    if has_audio:

        cmd = (
            f'ffmpeg -y '
            f'-i "{slideshow}" '
            f'-i "{audio}" '
            f'-vf "drawtext='
            f'textfile=\'{caption_file}\':'
            f'fontcolor=white:'
            f'fontsize=48:'
            f'box=1:'
            f'boxcolor=black@0.5:'
            f'boxborderw=10:'
            f'x=(w-text_w)/2:'
            f'y=h-150" '
            f'-c:v libx264 '
            f'-c:a aac '
            f'-shortest '
            f'"{output}"'
        )

    else:

        cmd = (
            f'ffmpeg -y '
            f'-i "{slideshow}" '
            f'-vf "drawtext='
            f'textfile=\'{caption_file}\':'
            f'fontcolor=white:'
            f'fontsize=48:'
            f'box=1:'
            f'boxcolor=black@0.5:'
            f'boxborderw=10:'
            f'x=(w-text_w)/2:'
            f'y=h-150" '
            f'-c:v libx264 '
            f'"{output}"'
        )
    print("=" * 100)
    print(cmd)
    print("=" * 100)
    print("caption_text =", repr(caption_text))
    print("output =", output) 
    print(caption_file)
    print(os.path.exists(caption_file))  
    if not run(cmd):
        return False

    return True