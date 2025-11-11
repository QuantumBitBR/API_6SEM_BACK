from google import genai

class GeminiService:
    def __init__(self):
        pass

    def generate_content(self, prompt: str) -> str:
        """
        Gera conteúdo usando o modelo Gemini.
        """
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text
