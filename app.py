from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from urllib.parse import unquote
import os

app = FastAPI()

# ✅ Mot de passe par défaut si non défini dans les variables d’environnement
API_PASSWORD = os.getenv("API_PASSWORD", "skystrem-support1@2mail.co")

@app.middleware("http")
async def check_api_password(request: Request, call_next):
    # On laisse passer la page racine sans auth (utile pour Hugging Face)
    if request.url.path == "/":
        return JSONResponse({"message": "Unity MediaFlow Proxy FR - IP France actif"})

    # Récupération du mot de passe dans les query params
    api_password = request.query_params.get("api_password")
    if api_password:
        api_password = unquote(api_password)  # %40 → @

    # Vérification
    if api_password == API_PASSWORD:
        return await call_next(request)

    # Sinon, 401 clair
    return JSONResponse(
        {"error": "Accès refusé : mot de passe incorrect ou manquant"},
        status_code=401
    )

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
