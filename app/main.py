from src.services import buscar_pais
from src.database import crear_tablas, guardar_pais, listar_paises_guardados

if __name__ == "__main__":
    crear_tablas()

    pais = buscar_pais("costa rica")
    if pais:
        print(f"{pais.name} - Capital: {pais.capital} - Población: {pais.population:,}")
        guardar_pais(pais)
        print("País guardado en la base de datos.")
    else:
        print("No se pudo obtener el país.")

    print("\nPaíses guardados hasta ahora:")
    for p in listar_paises_guardados():
        print(f"  - {p['nombre']} ({p['poblacion']:,} hab.)")