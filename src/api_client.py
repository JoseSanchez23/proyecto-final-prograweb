import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://api.restcountries.com/countries/v5")
API_KEY = os.getenv("API_KEY")


def _headers() -> dict:
    return {"Authorization": f"Bearer {API_KEY}"}


def get_all_countries() -> list | None:
    """Trae todos los países. Devuelve None si hay error."""
    return _get(BASE_URL)


def get_country_by_name(name: str) -> list | None:
    """Busca país(es) por nombre (búsqueda de texto libre)."""
    return _get(BASE_URL, params={"q": name})


def get_countries_by_region(region: str) -> list | None:
    """Trae países de una región (ej: 'Americas', 'Europe')."""
    return _get(BASE_URL, params={"region": region})


def _get(url: str, params: dict = None) -> list | None:
    """Conecta con la API externa y devuelve la lista de países ya parseada.
    Valida errores de conexión y respuestas vacías."""
    try:
        response = requests.get(url, params=params, headers=_headers(), timeout=10)
        response.raise_for_status()
        payload = response.json()
        objects = payload.get("data", {}).get("objects")
        if not objects:
            print(f"Advertencia: respuesta vacía desde {url}")
            return None
        return objects
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API ({url}): {e}")
        return None