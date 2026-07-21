import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://restcountries.com/v3.1")


def get_all_countries() -> list | None:
    """Trae todos los países. Devuelve None si hay error."""
    return _get(f"{BASE_URL}/all")


def get_country_by_name(name: str) -> list | None:
    """Busca país(es) por nombre común (ej: 'costa rica')."""
    return _get(f"{BASE_URL}/name/{name}")


def get_countries_by_region(region: str) -> list | None:
    """Trae países de una región (ej: 'americas', 'europe')."""
    return _get(f"{BASE_URL}/region/{region}")


def _get(url: str, params: dict = None) -> list | dict | None:
    """Conecta con la API externa y devuelve la respuesta ya parseada.
    Valida errores de conexión y respuestas vacías."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            print(f"Advertencia: respuesta vacía desde {url}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API ({url}): {e}")
        return None