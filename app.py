from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

app = FastAPI()
basic = HTTPBasic()

# Lit le mot de passe depuis les Secrets HF
API_PASSWORD = os.getenv("API_PASSWORD")

if not API_PASSWORD:
    raise RuntimeError("API_PASSWORD non défini dans les Secrets")

def check_auth(
    credentials: HTTPBasicCredentials = Depends(basic),
    authorization: str = Header(None)
):
    pwd = credentials.password
    if authorization and authorization.startswith("Bearer "):
        pwd = authorization[7:]
    
    if pwd == API_PASSWORD:
        return True
    raise HTTPException(status_code=401, detail="Mot de passe incorrect")

@app.get("/")
def root(auth = Depends(check_auth)):
    return {"message": "Unity MediaFlow Proxy FR - IP France actif"}

@app.get("/manifest.json")
def manifest(auth = Depends(check_auth)):
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.5.0",
        "name": "Unity MediaFlow Proxy FR",
        "description": "Proxy Real-Debrid IP France 2025 - Multi-comptes invisible",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg",
        "behaviorHints": {"adult": False, "configurable": False}
    }
