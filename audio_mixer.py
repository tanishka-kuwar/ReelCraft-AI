import subprocess


def mix_audio(voice_audio,
              music_audio,
              output_audio,
              music_volume):

    volume = music_volume / 100

    command = [

        "ffmpeg",
        "-y",

        "-i", voice_audio,
        "-i", music_audio,

        "-filter_complex",

        f"[1:a]volume={volume}[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first",

        "-c:a",

        "mp3",

        output_audio

    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        return False

    return True