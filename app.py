from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_PASSWORD = "skystrem-support1@2mail.co"

def check_password(authorization: str = Header(None)):
    if authorization != f"Bearer {API_PASSWORD}":
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    return True

@app.get("/")
def root():
    check_password()
    return {"message": "Unity MediaFlow Proxy FR - IP France actif"}

@app.get("/manifest.json")
def manifest():
    check_password()
    return {
        "id": "homeip.unity.mediaflow.proxy",
        "version": "1.1.0",
        "name": "Unity MediaFlow Proxy FR",
        "description": "Proxy Real-Debrid IP France 2025 - Multi-comptes invisible",
        "types": ["movie", "series", "channel"],
        "catalogs": [],
        "resources": ["catalog", "stream", "meta", "subtitles"],
        "logo": "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg",
        "behaviorHints": {"adult": False, "configurable": False}
    }
