from src.api_client import get_country_by_name, get_countries_by_region
from src.models import Country


def buscar_pais(nombre: str) -> Country | None:
    data = get_country_by_name(nombre)
    if not data:
        return None
    return Country.from_api_response(data[0])


def paises_por_region(region: str) -> list[Country]:
    data = get_countries_by_region(region)
    if not data:
        return []
    return [Country.from_api_response(p) for p in data]