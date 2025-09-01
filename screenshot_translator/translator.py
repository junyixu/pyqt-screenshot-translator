#!/usr/bin/env python3

import base64
from openai import OpenAI
from .config import API_KEY, BASE_URL, MODEL


def create_client():
    """Create and return OpenAI client with configured settings."""
    return OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )


def translate_image(image_path, prompt):
    """Translate text in image using the configured API."""
    client = create_client()
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }]
        }])

    return response.choices[0].message.content
