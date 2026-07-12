from google import genai
from dotenv import load_dotenv
from PIL import Image
import os
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_script(user_prompt):

    prompt = f"""
        Write a short engaging Instagram reel narration.

        User request:
        {user_prompt}

        Keep it 40-70 words.
        """

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt
    )

    return response.text

def generate_script_from_images(image_paths):
    prompt = """
        You are an expert Instagram Reel writer.

        Analyze ALL uploaded images.

        Generate 3 different narration options.

        Each narration should:
        - 40-70 words
        - Natural
        - Engaging
        - Mention what is visible in the images
        - Do NOT explain your reasoning.
        """

    contents = [prompt]

    for path in image_paths:
        img = Image.open(path)
        contents.append(img)

    for _ in range(3):

        try:

            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL"),
                contents=contents
            )

            return response.text.strip().lower()

        except Exception as e:

            print(e)

            time.sleep(2)

    raise Exception("Gemini is temporarily unavailable. Please try again.")

def generate_hashtags_from_images(image_paths):

    prompt = """
Analyze all uploaded images.

Generate 15 relevant Instagram hashtags.

Rules:
- Return only hashtags.
- One hashtag per line.
- No numbering.
- No explanation.
"""

    contents = [prompt]

    for path in image_paths:
        img = Image.open(path)
        contents.append(img)

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=contents
    )

    return response.text

def recommend_music(folder_path, input_files):

    prompt = """
Analyze the uploaded images.

Recommend ONLY ONE music category.

Choose exactly one from:

chill
travel
happy
cinematic
emotional
energetic

Return ONLY the category name.
"""

    contents = [prompt]

    for image in input_files:

        path = os.path.join(folder_path, image)

        with Image.open(path) as img:
            contents.append(img.copy())
        
    for _ in range(3):

        try:

            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL"),
                contents=contents
            )

            return response.text.strip().lower()
        
        except Exception as e:

            print("Gemini Error:", e)
            time.sleep(2)
    return "chill"

def order_images(folder_path, input_files):

    prompt = """
You are an expert storyteller.

Analyze all uploaded images.

Arrange them into the best chronological order for an Instagram Reel.

Return ONLY the image numbers separated by commas.

Example:
3,1,2

Do not explain anything.
"""

    contents = [prompt]

    for i, image in enumerate(input_files, start=1):
        contents.append(f"Image {i}")
        path = os.path.join(folder_path, image)

        with Image.open(path) as img:
            contents.append(img.copy())

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=contents
    )

    return response.text.strip()