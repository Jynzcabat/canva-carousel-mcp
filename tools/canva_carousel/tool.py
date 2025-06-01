import os
import requests

CANVA_API_KEY = os.getenv("CANVA_API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
LOGO_URL = os.getenv("LOGO_URL")

def generate_carousel(slides):
    headers = {
        "Authorization": f"Bearer {CANVA_API_KEY}",
        "Content-Type": "application/json"
    }

    placeholders = {
        f"slide{i+1}_title": slide.get("title", ""),
        f"slide{i+1}_text": slide.get("text", "")
        for i, slide in enumerate(slides)
    }

    if LOGO_URL:
        placeholders["logo"] = LOGO_URL

    payload = {
        "template_id": TEMPLATE_ID,
        "placeholders": placeholders
    }

    response = requests.post(
        "https://api.canva.com/v1/designs/from-template",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return {"url": response.json().get("url")}
    else:
        return {"error": response.text}
