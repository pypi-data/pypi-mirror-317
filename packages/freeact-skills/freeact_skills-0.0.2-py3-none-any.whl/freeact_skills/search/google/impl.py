import os

from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool

SEARCH = Tool(google_search=GoogleSearch())


def search(query: str, api_key: str | None = None):
    client = genai.Client(
        api_key=api_key or os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1alpha"},
    )
    for chunk in client.models.generate_content_stream(
        contents=query,
        model="gemini-2.0-flash-exp",
        config=GenerateContentConfig(
            temperature=0.0,
            tools=[SEARCH],
        ),
    ):
        print(chunk.text, end="", flush=True)
