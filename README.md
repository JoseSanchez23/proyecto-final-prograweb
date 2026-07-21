# WorldExplorer — Aplicación conectada a REST Countries API

## Descripción

Aplicación que consume la [REST Countries API (v5)](https://restcountries.com/docs/countries) para obtener información de países (capital, población, moneda, idioma, bandera, etc.), procesa los datos y los almacena en una base de datos local SQLite.

**Producto:** buscador/dashboard de países orientado a viajeros, estudiantes de geografía y personas interesadas en explorar datos geográficos de forma rápida.

## Arquitectura

```
REST Countries API (v5)
        ↓
api_client.py   → conexión a la API, manejo de errores y respuestas vacías
        ↓
models.py       → transforma el JSON crudo en un objeto Country tipado
        ↓
services.py     → combina api_client + models en funciones de alto nivel
        ↓
database.py     → guarda/actualiza los objetos Country en SQLite
        ↓
main.py         → punto de entrada, orquesta el flujo completo
```

## Estructura del repositorio

```
proyecto-final-prograweb/
├── requirements.txt
├── .env.example
├── src/
│   ├── api_client.py    conexión con la API
│   ├── models.py        modelo de datos (Country)
│   ├── database.py      persistencia en SQLite
│   └── services.py      lógica de negocio
├── app/
│   └── main.py           punto de entrada
├── tests/
│   └── test_api_client.py
└── docs/
    └── arquitectura.md
```

## Requisitos

- Python 3.10 o superior
- Git
- API key de REST Countries (gratuita, sin tarjeta — ver sección "Configuración")

## Instalación

```bash
git clone https://github.com/TU_USUARIO/proyecto-final-prograweb.git
cd proyecto-final-prograweb
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración de la API key

1. Registrarse en https://restcountries.com/sign-up y obtener una API key (free tier: 500 requests/mes, sin tarjeta).
2. Copiar el archivo de variables de entorno de ejemplo:
```bash
   cp .env.example .env
```
3. Abrir el archivo `.env` recién creado y completarlo con la key del equipo (compartida por canal privado, nunca por GitHub):
```
   API_BASE_URL=https://api.restcountries.com/countries/v5
   API_KEY=rc_live_xxxxxxxxxxxx
```

El archivo `.env` está excluido del repositorio mediante `.gitignore` (línea ya incluida en la plantilla Python). Cada integrante mantiene su propia copia local con la key adentro; nunca se sube a GitHub.

## Ejecución

```bash
python -m app.main
```

Salida esperada:
```
Costa Rica - Capital: San José - Población: 5,160,700
País guardado en la base de datos.

Países guardados hasta ahora:
  - Costa Rica (5,160,700 hab.)
```

**Nota:** ejecutar siempre con `python -m app.main`, no `python app/main.py`. La flag `-m` agrega la raíz del proyecto a la ruta de búsqueda de módulos; sin ella, la importación `from src...` falla con `ModuleNotFoundError: No module named 'src'`.

La base de datos (`paises.db`) se genera automáticamente en la primera ejecución y no se sube al repositorio.

## Flujo de trabajo en Git

```bash
git pull origin main                              # antes de empezar a trabajar
git checkout -b feature/nombre-de-la-tarea         # para cada tarea nueva
git add .
git commit -m "feat: descripción del cambio"
git push origin feature/nombre-de-la-tarea         # luego, Pull Request hacia main
```

## Problemas comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Se ejecutó `python app/main.py` en vez de `-m` | Usar `python -m app.main` |
| Import de `requests`/`dotenv` marcado en el editor | VS Code usando un intérprete distinto al del `venv` | `Cmd/Ctrl+Shift+P` → "Python: Select Interpreter" → seleccionar `./venv/bin/python` |
| `KeyError` al procesar la respuesta de la API | Respuesta de error o formato inesperado | Imprimir la respuesta cruda antes de parsear, para confirmar su estructura |