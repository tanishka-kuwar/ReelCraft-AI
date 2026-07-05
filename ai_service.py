from google import genai
from dotenv import load_dotenv
import os

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