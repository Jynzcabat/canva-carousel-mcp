import os
import base64
import hashlib
import secrets
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import httpx

app = FastAPI()

# Génère un code_verifier et son code_challenge associé
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()

@app.get("/authorize")
def authorize():
    url = "https://www.canva.com/oauth2/authorize"
    params = {
        "client_id": os.getenv("CANVA_CLIENT_ID"),
        "redirect_uri": os.getenv("CANVA_REDIRECT_URI"),
        "response_type": "code",
        "scope": "openid email",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return RedirectResponse(f"{url}?{query_string}")

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse(content={"error": "Missing 'code' in query parameters."}, status_code=400)

    token_url = "https://www.canva.com/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("CANVA_REDIRECT_URI"),
        "client_id": os.getenv("CANVA_CLIENT_ID"),
        "code_verifier": code_verifier
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        return JSONResponse(content=response.json())
