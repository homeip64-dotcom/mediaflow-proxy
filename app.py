from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import urllib.parse  # ← pour décoder le mot de passe encodé dans l’URL

app = FastAPI()
basic = HTTPBasic()
API_PASSWORD = os.getenv("API_PASSWORD")

if not API_PASSWORD:
    raise RuntimeError("API_PASSWORD non défini")

def check_auth(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(basic),
    authorization: str = Header(None)
):
    # Debug log
    print("DEBUG PARAMS:", request.query_params)

    # 1️⃣ BASIC AUTH
    if credentials and credentials.password == API_PASSWORD:
        return True

    # 2️⃣ BEARER TOKEN
    if authorization and authorization.startswith("Bearer ") and authorization[7:] == API_PASSWORD:
        return True

    # 3️⃣ QUERY PARAM (MediaFusion)
    query_pass = request.query_params.get("api_password")
    if query_pass:
        decoded_pass = urllib.parse.unquote(query_pass)
        if decoded_pass == API_PASSWORD:
            return True

    # Rien ne correspond → 401
    raise HTTPException(status_code=401, detail="Mot de passe incorrect")

# --- ROUTES ---

@app.get("/")
def root(auth = Depends(check_auth)):
    return {"message": "Unity MediaFlow Proxy FR - IP France actif"}

@app.get("/proxy/ip")
def proxy_ip(auth = Depends(check_auth)):
    return {"status": "ok", "message": "Validation MediaFlow réussie"}

@app.get("/manifest.json")
def manifest(auth = Depends(check_auth)):
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.6.2",
        "name": "Unity MediaFlow Proxy FR",
        "description": "Proxy Real-Debrid IP France 2025 - Multi-comptes invisible",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg",
        "behaviorHints": {"adult": False, "configurable": False}
    }
