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
            return response.text

        except Exception as e:
            if "503" in str(e):
                time.sleep(2)
            else:
                raise

    raise Exception("Gemini is busy. Please try again in a few seconds.")