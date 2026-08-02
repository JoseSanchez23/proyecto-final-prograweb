from .api_client import get_country_by_name, get_countries_by_region
from .models import Country
from .database import guardar_pais


def buscar_pais(nombre: str) -> Country | None:
    data = get_country_by_name(nombre)
    if not data:
        return None
    pais = Country.from_api_response(data[0])
    _guardar_pais_con_reintento(pais)
    return pais


def _guardar_pais_con_reintento(pais: Country, intentos: int = 2):
    """Intenta guardar el país en Supabase, pero si falla (p. ej. por un hipo de
    red típico de entornos serverless), no bloquea la búsqueda del usuario.
    El historial es una funcionalidad secundaria; la prioridad es mostrar el país."""
    import time
    for intento in range(intentos):
        try:
            guardar_pais(pais)
            return
        except Exception as e:
            print(f"Aviso: no se pudo guardar '{pais.name}' en Supabase (intento {intento + 1}/{intentos}): {e}")
            if intento < intentos - 1:
                time.sleep(0.3)
    print(f"Aviso: '{pais.name}' no se guardó en el historial tras {intentos} intentos, pero la búsqueda continúa.")


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