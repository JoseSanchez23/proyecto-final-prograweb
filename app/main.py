from src.services import buscar_pais

if __name__ == "__main__":
    pais = buscar_pais("costa rica")
    if pais:
        print(f"{pais.name} - Capital: {pais.capital} - Población: {pais.population:,}")
    else:
        print("No se pudo obtener el país.")