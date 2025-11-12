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
import httpx
from fastapi.responses import JSONResponse

TORRENTIO_BASE = "https://torrentio.strem.fun"

@app.get("/proxy/{path:path}")
async def proxy_to_torrentio(path: str, request: Request, auth = Depends(check_api_password)):
    """
    Proxy universel pour Torrentio via MediaFlow FR
    Permet de faire suivre toutes les requêtes vers torrentio.strem.fun
    avec authentification et IP française.
    """
    target_url = f"{TORRENTIO_BASE}/{path}"

    # Ajoute les query params (ex: providers, qualityfilter, etc.)
    if request.query_params:
        target_url += f"?{request.query_params}"

    async with httpx.AsyncClient() as client:
        r = await client.get(target_url)

    # Retourne la même réponse JSON que Torrentio
    return JSONResponse(content=r.json(), status_code=r.status_code)
