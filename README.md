# WorldExplorer — Aplicación conectada a REST Countries API

## Descripción

Aplicación que consume la [REST Countries API (v5)](https://restcountries.com/docs/countries) para obtener información de países (capital, población, moneda, idioma, bandera, etc.), procesa los datos y los almacena en una base de datos local SQLite.

**Producto:** buscador/dashboard de países orientado a viajeros, estudiantes de geografía y personas interesadas en explorar datos geográficos de forma rápida.

## Arquitectura

```
REST Countries API (v5)
↓
api_client.py → conexión a la API, manejo de errores y respuestas vacías
↓
models.py → transforma el JSON crudo en un objeto Country tipado
↓
services.py → combina api_client + models en funciones de alto nivel
↓
database.py → guarda/actualiza los objetos Country en SQLite
↓
main.py → punto de entrada, orquesta el flujo completo
```

## Estructura del repositorio

```
proyecto-final-prograweb/
├── requirements.txt
├── env_example
├── src/
│   ├── api_client.py    conexión con la API
│   ├── models.py        modelo de datos (Country)
│   ├── database.py      persistencia en SQLite
│   └── services.py      lógica de negocio
├── app/
│   ├── main.py           punto de entrada (backend consola)
│   └── server.py         servidor web (Flask)
├── templates/
│   └── index.html        interfaz web
├── static/
│   ├── css/
│   │   └── styles.css    estilos de la interfaz
│   └── js/
│       └── app.js        lógica del frontend
├── tests/
│   └── test_api_client.py
└── docs/
    └── arquitectura.md
```

## Requisitos

- Python 3.10 o superior
- Git
- API key de REST Countries (gratuita, sin tarjeta — ver sección "Configuración")
- Conexión a internet (para consultar la API)

### Dependencias del proyecto

Las dependencias se instalan automáticamente con `pip install -r requirements.txt`:

- `requests` → Para consumir la API de países.
- `python-dotenv` → Para manejar las variables de entorno.
- `flask` → Para el servidor web y la API interna.
- `pytest` → Para ejecutar las pruebas unitarias.

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
cp env_example .env
```
3. Abrir el archivo `.env` recién creado y completarlo con tu API key:
```
API_BASE_URL=https://api.restcountries.com/countries/v5
API_KEY=tu_api_key_aqui
```

El archivo `.env` está excluido del repositorio mediante `.gitignore`. Cada integrante mantiene su propia copia local con la key adentro; nunca se sube a GitHub.

> **Para pruebas rápidas:** Puedes usar la demo key oficial de REST Countries que no requiere registro:
> ```
> API_KEY=rc_live_demo
> ```
> (Tiene limitaciones, pero es útil para probar la interfaz sin necesidad de crear una cuenta)

## Ejecución

El proyecto tiene dos modos de ejecución: el **backend en consola** (para pruebas y desarrollo) y el **servidor web completo** (para usar la interfaz gráfica).

### 1. Backend en consola (modo básico)

Ejecuta el siguiente comando para buscar un país y ver los datos en la terminal:

```bash
python -m app.main --search "Costa Rica"
```

**Salida esperada:**
```
Bienvenido a World Explorer - backend educativo.
Usa --search, --region o --compare para obtener datos.

Resultado de búsqueda para 'Costa Rica':
----------------------------------------
Nombre: Costa Rica
Nombre oficial: Republic of Costa Rica
Capital: San José
Población: 5,160,700
...
Este país se guardó en la base de datos local.

Países guardados en la base de datos:
  - Costa Rica (5,160,700 hab.)
```

**Nota:** ejecutar siempre con `python -m app.main`, no `python app/main.py`. La flag `-m` agrega la raíz del proyecto a la ruta de búsqueda de módulos; sin ella, la importación `from src...` falla con `ModuleNotFoundError: No module named 'src'`.

La base de datos (`paises.db`) se genera automáticamente en la primera ejecución y no se sube al repositorio.

### 2. Servidor web (modo completo con interfaz gráfica)

Este modo inicia un servidor Flask que sirve la interfaz web y la API. Es el modo recomendado para usar la aplicación.

#### Paso 1: Instalar dependencias (incluye Flask)

Asegúrate de tener todas las dependencias instaladas:

```bash
pip install -r requirements.txt
```

> **Nota:** Si ves un error `ModuleNotFoundError: No module named 'flask'`, ejecuta `pip install flask` manualmente.

#### Paso 2: Configurar tu API key

Asegúrate de que el archivo `.env` esté configurado con tu API key (como se explicó en la sección "Configuración de la API key").

#### Paso 3: Ejecutar el servidor web

```bash
python -m app.server
```

**Verás un mensaje como:**
```
🌍 WorldExplorer - Servidor Web
📁 Ruta del proyecto: /Users/...
📡 Servidor corriendo en: http://localhost:5001
🔍 Prueba: http://localhost:5001/api/countries/search?name=Costa%20Rica
🔄 Presiona Ctrl+C para detener el servidor
```

#### Paso 4: Abrir la aplicación en el navegador

1. Ve a `http://localhost:5001`
2. Busca un país (ej. "Costa Rica")
3. Prueba el comparador con dos países (ej. "Costa Rica" y "México")

#### Paso 5: Probar los endpoints de la API (opcional)

Puedes probar la API directamente en el navegador o con `curl`:

| Endpoint | Ejemplo |
| :--- | :--- |
| Buscar país | `http://localhost:5001/api/countries/search?name=Costa%20Rica` |
| Comparar países | `http://localhost:5001/api/countries/compare?country1=Costa%20Rica&country2=Mexico` |
| Países guardados | `http://localhost:5001/api/countries/saved` |

**Ejemplo con `curl`:**
```bash
curl "http://localhost:5001/api/countries/search?name=Costa%20Rica"
```

#### Paso 6: Detener el servidor

Presiona `Ctrl+C` en la terminal donde está corriendo Flask.

## Pruebas

Para ejecutar las pruebas unitarias y verificar que la conexión a la API funciona correctamente:

```bash
python -m pytest tests/
```

**Salida esperada:**
```
============================= test session starts ==============================
collected 2 items
tests/test_api_client.py ..                                              [100%]
============================== 2 passed in 0.5s ===============================
```

Si alguna prueba falla, verifica que el archivo `.env` esté correctamente configurado con la API Key.

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
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'src'` | Se ejecutó `python app/main.py` en vez de `-m` | Usar `python -m app.main` |
| `ModuleNotFoundError: No module named 'flask'` | Flask no está instalado | Ejecutar `pip install flask` o `pip install -r requirements.txt` |
| Import de `requests`/`dotenv` marcado en el editor | VS Code usando un intérprete distinto al del `venv` | `Cmd/Ctrl+Shift+P` → "Python: Select Interpreter" → seleccionar `./venv/bin/python` |
| `KeyError` al procesar la respuesta de la API | Respuesta de error o formato inesperado | Imprimir la respuesta cruda antes de parsear, para confirmar su estructura |
| `Address already in use` | El puerto 5001 está ocupado | Cambiar el puerto en `app/server.py` (línea 80) a `port=5002` |
| La página no tiene estilos | Rutas incorrectas en `index.html` | Verificar que sean `/static/css/styles.css` y `/static/js/app.js` |
| La API devuelve error 404 | La API key es inválida o no está configurada | Verificar el archivo `.env` o usar `API_KEY=rc_live_demo` |

## Documentación adicional

Para una explicación detallada de la arquitectura, el flujo de datos, las decisiones de diseño y la visión futura con frontend web, consulta el archivo [docs/arquitectura.md](docs/arquitectura.md).