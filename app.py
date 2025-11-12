from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

# TON MOT DE PASSE (celui que tu voulais)
API_PASSWORD = "skystrem-support1@2mail.co"

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    return True

@app.get("/")
def read_root(auth: bool = Depends(verify_password)):
    return {"message": "Hello from MediaFlow Proxy! Accès autorisé."}

@app.get("/manifest.json")
def manifest(auth: bool = Depends(verify_password)):
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.0.5",
        "name": "Unity MediaFlow Proxy",
        "description": "Proxy IP France 2025 - Simultané illimité Real-Debrid",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "idPrefixes": [""],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg",
        "behaviorHints": {
            "adult": False,
            "configurable": False
        }
    }