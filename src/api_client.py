import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://api.restcountries.com/countries/v5")
API_KEY = os.getenv("API_KEY")


def _headers() -> dict:
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def get_all_countries(limit: int = 100, offset: int = 0, response_fields: str | None = None) -> list | None:
    """Trae países usando el endpoint de lista paginada."""
    params = {"limit": limit, "offset": offset}
    if response_fields:
        params["response_fields"] = response_fields
    return _get(BASE_URL, params=params)


def get_country_by_name(name: str) -> list | None:
    """Busca país(es) por nombre usando búsqueda libre (q)."""
    if not name or not name.strip():
        return None
    return _get(BASE_URL, params={"q": name})


def get_countries_by_region(region: str) -> list | None:
    """Trae países de una región específica."""
    if not region or not region.strip():
        return None
    return _get(BASE_URL, params={"region": region})


def _get(url: str, params: dict | None = None) -> list | None:
    """Conecta con la API externa y devuelve la lista de países ya parseada."""
    try:
        response = requests.get(url, params=params, headers=_headers(), timeout=10)
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data")
        if not isinstance(data, dict):
            print(f"Advertencia: la respuesta desde {url} no contiene 'data'.")
            return None
        objects = data.get("objects")
        if objects is None:
            print(f"Advertencia: la respuesta desde {url} no contiene 'data.objects'.")
            return None
        if not isinstance(objects, list):
            print(f"Advertencia: 'data.objects' desde {url} no es una lista.")
            return None
        return objects
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API ({url}): {e}")
        return None
    except ValueError as e:
        print(f"Error al parsear JSON desde {url}: {e}")
        return None