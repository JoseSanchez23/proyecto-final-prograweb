import os
from dotenv import load_dotenv
from supabase import create_client
from src.models import Country

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# El backend usa la service_role key porque corre en el servidor,
# nunca en el navegador del usuario, y necesita poder escribir.
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def crear_tablas():
    """La tabla ya se crea manualmente en Supabase (SQL Editor), no aquí."""
    pass


def guardar_pais(pais: Country):
    """Inserta o actualiza un país en Supabase."""
    supabase.table("paises").upsert({
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
    response = supabase.table("paises").select("*").eq("nombre", nombre).execute()
    data = response.data
    return data[0] if data else None


def listar_paises_guardados() -> list[dict]:
    """Devuelve todos los países guardados como lista de diccionarios."""
    response = supabase.table("paises").select("*").order("nombre").execute()
    return response.data