import argparse
from src.services import buscar_pais, buscar_paises_por_region, comparar_paises
from src.database import crear_tablas, guardar_pais, listar_paises_guardados


def imprimir_pais(pais):
    print("----------------------------------------")
    print(f"Nombre: {pais.name}")
    print(f"Nombre oficial: {pais.official_name}")
    print(f"Capital: {pais.capital}")
    print(f"Región: {pais.region}")
    print(f"Subregión: {pais.subregion}")
    print(f"Continentes: {', '.join(pais.continents) if pais.continents else 'N/A'}")
    print(f"Población: {pais.population:,}")
    print(f"Área: {pais.area_km2:,} km²")
    print(f"Moneda: {pais.currency}")
    print(f"Idioma(s): {pais.language}")
    print(f"Bandera: {pais.flag_url}")
    if pais.emoji_flag:
        print(f"Emoji de bandera: {pais.emoji_flag}")
    print("----------------------------------------\n")


def main():
    parser = argparse.ArgumentParser(
        description="World Explorer - backend educativo para buscar y comparar países"
    )
    parser.add_argument("--search", "-s", help="Buscar un país por nombre")
    parser.add_argument("--region", "-r", help="Listar países de una región")
    parser.add_argument(
        "--compare",
        "-c",
        nargs="+",
        help="Comparar varios países por nombre",
    )
    args = parser.parse_args()

    crear_tablas()

    if args.search:
        pais = buscar_pais(args.search)
        if pais:
            print(f"Resultado de búsqueda para '{args.search}':")
            imprimir_pais(pais)
            guardar_pais(pais)
            print("Este país se guardó en la base de datos local.")
        else:
            print(f"No se encontró ningún país para '{args.search}'.")
    elif args.region:
        paises = buscar_paises_por_region(args.region)
        if paises:
            print(f"Países encontrados en la región '{args.region}':")
            for pais in paises[:10]:
                print(f"- {pais.name} ({pais.capital})")
            print("\nSe guardan solo consultas individuales, no la lista completa.")
        else:
            print(f"No se encontraron países para la región '{args.region}'.")
    elif args.compare:
        paises = comparar_paises(args.compare)
        if paises:
            print("Comparación de países:")
            for pais in paises:
                imprimir_pais(pais)
        else:
            print("No se encontraron países para comparar.")
    else:
        print("Bienvenido a World Explorer - backend educativo.")
        print("Usa --search, --region o --compare para obtener datos.")
        print("Ejemplo: python -m app.main --search \"Costa Rica\"")

    print("\nPaíses guardados en la base de datos:")
    for p in listar_paises_guardados():
        print(f"  - {p['nombre']} ({p['poblacion']:,} hab.)")


if __name__ == "__main__":
    main()