from __future__ import annotations

import os
from dataclasses import dataclass

import aiohttp
import requests

from verbia_core.error import VerbiaError

GEMINI_1_5_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@dataclass
class GenerationConfig:
    response_mime_type: str | None = None


class GeminiClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def generate_content(self, prompt: str, generation_config: GenerationConfig | None = None) -> str:
        body = {}
        if generation_config:
            body["generationConfig"] = {}
            if generation_config.response_mime_type:
                body["generationConfig"]["response_mime_type"] = generation_config.response_mime_type
        body["contents"] = [{
            "parts": [
                {"text": prompt}
            ]
        }]
        response = requests.post(
            url=GEMINI_1_5_URL,
            params={"key": self._api_key},
            headers={"Content-Type": "application/json"},
            json=body
        )
        if response.status_code != 200:
            raise Exception(f"Failed to generate content: {response.text}")
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]


    async def generate_content_async(self, prompt: str, generation_config: GenerationConfig | None = None) -> str:
        body = {}
        if generation_config:
            body["generationConfig"] = {}
            if generation_config.response_mime_type:
                body["generationConfig"]["response_mime_type"] = generation_config.response_mime_type
        body["contents"] = [{
            "parts": [
                {"text": prompt}
            ]
        }]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=GEMINI_1_5_URL,
                params={"key": self._api_key},
                headers={"Content-Type": "application/json"},
                json=body
            ) as response:
                if response.status != 200:
                    raise Exception(f"Failed to generate content: {await response.text()}")
                response_json = await response.json()
                return response_json["candidates"][0]["content"]["parts"][0]["text"]

def get_client(api_key: str) -> GeminiClient:

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise VerbiaError("GEMINI_API_KEY required.")
    return GeminiClient(api_key)
