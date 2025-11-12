from fastapi import FastAPI, Request, HTTPException
from urllib.parse import unquote
import os

app = FastAPI()

# Mot de passe d’accès
API_PASSWORD = os.getenv("API_PASSWORD", "skystrem-support1@2mail.co")

@app.middleware("http")
async def check_api_password(request: Request, call_next):
    query_params = dict(request.query_params)
    api_password = query_params.get("api_password")

    # On décode les caractères URL (%40 → @)
    if api_password:
        api_password = unquote(api_password)

    # Vérification
    if api_password == API_PASSWORD:
        response = await call_next(request)
        return response

    # Sinon, renvoie 401
    raise HTTPException(status_code=401, detail="Accès refusé : mot de passe incorrect")

@app.get("/")
def root():
    return {"message": "Unity MediaFlow Proxy FR - IP France actif"}

@app.get("/proxy/ip")
def proxy_ip():
    return {"status": "ok", "message": "Validation MediaFlow réussie"}

@app.get("/manifest.json")
def manifest():
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.6.0",
        "name": "Unity MediaFlow Proxy FR",
        "description": "Proxy Real-Debrid IP France 2025 - Multi-comptes invisible",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg",
        "behaviorHints": {"adult": False, "configurable": False}
    }
