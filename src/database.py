import os
from dotenv import load_dotenv
from supabase import create_client, Client
from src.models import Country

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

_supabase_client: Client | None = None


def get_client() -> Client:
    """Crea el cliente de Supabase de forma perezosa (lazy), dentro de cada invocación
    de la función serverless, en vez de crearlo una sola vez al importar el módulo.
    Esto evita el error 'ConnectError: [Errno 16] Device or resource busy' que ocurre
    cuando AWS Lambda reutiliza un contenedor "congelado" con conexiones TCP stale."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _supabase_client


def crear_tablas():
    """La tabla ya se crea manualmente en Supabase (SQL Editor), no aquí."""
    pass


def guardar_pais(pais: Country):
    """Inserta o actualiza un país en Supabase."""
    get_client().table("paises").upsert({
        "nombre": pais.name,
        "nombre_oficial": pais.official_name,
        "capital": pais.capital,
        "region": pais.region,
        "subregion": pais.subregion,
        "poblacion": pais.population,
        "area_km2": pais.area_km2,
        "moneda": pais.currency,
        "idioma": pais.language,
        "bandera_url": pais.flag_url,
    }, on_conflict="nombre").execute()


def obtener_pais_guardado(nombre: str) -> dict | None:
    response = get_client().table("paises").select("*").eq("nombre", nombre).execute()
    data = response.data
    return data[0] if data else None


def listar_paises_guardados() -> list[dict]:
    """Devuelve todos los países guardados como lista de diccionarios."""
    response = get_client().table("paises").select("*").order("nombre").execute()
    return response.data