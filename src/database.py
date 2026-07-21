import sqlite3
from src.models import Country

DB_PATH = "paises.db"


def crear_tablas():
    """Crea la tabla de países si no existe todavía."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            nombre_oficial TEXT,
            capital TEXT,
            region TEXT,
            subregion TEXT,
            poblacion INTEGER,
            area_km2 REAL,
            moneda TEXT,
            idioma TEXT,
            bandera_url TEXT,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def guardar_pais(pais: Country):
    """Inserta o actualiza un país en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO paises
            (nombre, nombre_oficial, capital, region, subregion,
             poblacion, area_km2, moneda, idioma, bandera_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(nombre) DO UPDATE SET
            nombre_oficial = excluded.nombre_oficial,
            capital = excluded.capital,
            region = excluded.region,
            subregion = excluded.subregion,
            poblacion = excluded.poblacion,
            area_km2 = excluded.area_km2,
            moneda = excluded.moneda,
            idioma = excluded.idioma,
            bandera_url = excluded.bandera_url,
            fecha_actualizacion = CURRENT_TIMESTAMP
    """, (
        pais.name, pais.official_name, pais.capital, pais.region,
        pais.subregion, pais.population, pais.area_km2,
        pais.currency, pais.language, pais.flag_url,
    ))
    conn.commit()
    conn.close()


def listar_paises_guardados() -> list[dict]:
    """Devuelve todos los países guardados como lista de diccionarios."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paises")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]