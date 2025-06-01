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

    # On initialise un dictionnaire vide
    placeholders = {}

    # Pour chaque slide, on ajoute 2 clés : titre + texte
    for i, slide in enumerate(slides):
        placeholders[f"slide{i+1}_title"] = slide.get("title", "")
        placeholders[f"slide{i+1}_text"] = slide.get("text", "")

    # Si le logo est défini, on l’ajoute
    if LOGO_URL:
        placeholders["logo"] = LOGO_URL

    # On construit la requête pour Canva
    payload = {
        "template_id": TEMPLATE_ID,
        "placeholders": placeholders
    }

    response = requests.post(
        "https://api.canva.com/v1/designs/from-template",
        headers=headers,
        json=payload
    )

    # Gestion de la réponse
    if response.status_code == 200:
        return {"url": response.json().get("url")}
    else:
        return {"error": response.text}
