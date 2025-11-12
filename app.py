from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException

app = FastAPI()
security = HTTPBasic()

API_PASSWORD = "skystrem-support1@2mail.co"

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    # On ignore totalement le username, on ne vérifie QUE le password
    if credentials.password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    return True

@app.get("/")
@Depends(verify_password)
def root():
    return {"message": "Unity MediaFlow Proxy FR - IP France actif"}

@app.get("/manifest.json")
@Depends(verify_password)
def manifest():
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.2.1",
        "name": "Unity MediaFlow Proxy FR",
        "description": "Proxy Real-Debrid IP France 2025 - Multi-comptes invisible",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg",
        "behaviorHints": {"adult": False, "configurable": False}
    }
