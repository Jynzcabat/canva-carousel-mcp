import os
import secrets
import hashlib
import base64
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import httpx
import urllib.parse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="une-clé-super-secrète")

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return code_verifier, code_challenge

@app.get("/authorize")
async def authorize(request: Request):
    code_verifier, code_challenge = generate_pkce_pair()
    request.session["code_verifier"] = code_verifier

    params = {
        "client_id": os.getenv("CANVA_CLIENT_ID"),
        "redirect_uri": os.getenv("CANVA_REDIRECT_URI"),
        "response_type": "code",
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
        "scope": "openid email",
    }

    url = f"https://www.canva.com/api/oauth/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing 'code' in query parameters."}

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

        try:
            json_data = response.json()
        except Exception as e:
            return {
                "error": "Failed to decode JSON response from Canva",
                "status_code": response.status_code,
                "response_text": response.text,
            }

    return json_data

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)
        return response.json()
