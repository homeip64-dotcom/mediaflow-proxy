from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_PASSWORD = "skystrem-support1@2mail.co"

def check_password(authorization: str = Header(None)):
    if authorization != f\"Bearer {API_PASSWORD}\":
        raise HTTPException(status_code=401, detail=\"Mot de passe incorrect\")
    return True

@app.get("/")
def root():
    return {\"message\": \"Proxy actif - IP France\"}

@app.get(\"/manifest.json\")
def manifest():
    return {
        \"id\": \"homeip.unity.mediaflow.proxy\",
        \"version\": \"1.0.9\",
        \"name\": \"Unity MediaFlow Proxy FR\",
        \"description\": \"Proxy IP France 2025 - Real-Debrid illimité\",
        \"types\": [\"movie\", \"series\", \"channel\"],
        \"catalogs\": [],
        \"resources\": [\"catalog\", \"stream\", \"meta\", \"subtitles\"],
        \"logo\": \"https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/fr.svg\",
        \"behaviorHints\": {\"adult\": False, \"configurable\": False}
    }

# Applique le check seulement sur les routes protégées
root = check_password(root)
manifest = check_password(manifest)
