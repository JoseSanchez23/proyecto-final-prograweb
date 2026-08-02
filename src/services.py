from .api_client import get_country_by_name, get_countries_by_region
from .models import Country
from .database import guardar_pais

def buscar_pais(nombre: str) -> Country | None:
    data = get_country_by_name(nombre)
    if not data:
        return None
    pais = Country.from_api_response(data[0])
    guardar_pais(pais)
    return pais


def buscar_paises_por_region(region: str) -> list[Country]:
    data = get_countries_by_region(region)
    if not data:
        return []
    return [Country.from_api_response(p) for p in data]


def comparar_paises(nombres: list[str]) -> list[Country]:
    resultados: list[Country] = []
    for nombre in nombres:
        pais = buscar_pais(nombre)
        if pais:
            resultados.append(pais)
    return resultados


def buscar_paises(nombre: str) -> list[Country]:
    data = get_country_by_name(nombre)
    if not data:
        return []
    return [Country.from_api_response(p) for p in data]