# main.py

import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import httpx
import urllib.parse

app = FastAPI()

@app.get("/authorize")
def authorize():
    base_url = "https://www.canva.com/oauth2/authorize"
    params = {
        "client_id": os.getenv("CANVA_CLIENT_ID"),
        "redirect_uri": os.getenv("CANVA_REDIRECT_URI"),
        "response_type": "code",
        "scope": "openid email",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    token_url = "https://www.canva.com/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("CANVA_REDIRECT_URI"),
        "client_id": os.getenv("CANVA_CLIENT_ID"),
        "client_secret": os.getenv("CANVA_CLIENT_SECRET"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)
        return response.json()
