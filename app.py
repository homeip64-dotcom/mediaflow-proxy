from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

app = FastAPI()
basic = HTTPBasic()
API_PASSWORD = os.getenv("API_PASSWORD")

if not API_PASSWORD:
    raise RuntimeError("API_PASSWORD non défini")

def check_auth(
    credentials: HTTPBasicCredentials = Depends(basic),
    authorization: str = Header(None)
):
    # PRIORITÉ BASIC AUTH (Stremio) → marche à tous les coups
    if credentials and credentials.password == API_PASSWORD:
        return True
    # Fallback Bearer (navigateur)
    if authorization and authorization.startswith("Bearer ") and authorization[7:] == API_PASSWORD:
        return True
    raise HTTPException(status_code=401, detail="Mot de passe incorrect")

@app.get("/")
def root(auth = Depends(check_auth)):
    return {"message": "Unity MediaFlow Proxy FR - IP France actif"}

@app.get("/manifest.json")
def manifest(auth = Depends(check_auth)):
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.6.0",
        "name": "Unity MediaFlow Proxy FR",
        "description": "Proxy Real-Debrid IP France 2025 - Multi-comptes invisible",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3    fr.svg",
        "behaviorHints": {"adult": False, "configurable": False}
    }
