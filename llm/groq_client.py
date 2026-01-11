import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, prompt, temperature=0.2):
        response = self.client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),   # ✅ STABLE MODEL
            messages=[
                {"role": "system", "content": "You are a precise academic research assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content
