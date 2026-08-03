# WorldExplorer — Aplicación conectada a REST Countries API

## Descripción

Aplicación que consume la [REST Countries API (v5)](https://restcountries.com/docs/countries) para obtener información de países (capital, población, moneda, idioma, bandera, etc.), procesa los datos y los almacena en **Supabase** (PostgreSQL en la nube).

**Producto:** buscador/dashboard de países orientado a viajeros, estudiantes de geografía y personas interesadas en explorar datos geográficos de forma rápida.

## Integrantes del grupo

- [Iván Cespedes]
- [Mauro Hernandez]
- [Yulissa Navarro]
- [Jose Ignacio Sánchez]

## Link de producción

🔗 [Abrir WorldExplorer en Vercel](https://proyecto-final-prograweb.vercel.app)

## Arquitectura

```
REST Countries API (v5)
↓
api_client.py → conexión a la API, manejo de errores y respuestas vacías
↓
models.py → transforma el JSON crudo en un objeto Country tipado
↓
services.py → combina api_client + models en funciones de alto nivel;
              guarda cada país consultado en la base de datos
↓
database.py → guarda/actualiza los objetos Country en Supabase (PostgreSQL)
↓
server.py → servidor Flask, expone la interfaz web y la API interna
```

> Nota: `database.py` migró de SQLite a Supabase. SQLite no es compatible con el entorno serverless de Vercel, ya que su sistema de archivos no persiste entre ejecuciones.

## Estructura del repositorio

```
proyecto-final-prograweb/
├── requirements.txt
├── env_example
├── vercel.json           configuración de despliegue en Vercel
├── src/
│   ├── api_client.py    conexión con la API
│   ├── models.py        modelo de datos (Country)
│   ├── database.py      persistencia en Supabase
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

## Tecnologías utilizadas

- **Backend:** Python 3, Flask
- **Fuente de datos:** REST Countries API (v5)
- **Base de datos:** Supabase (PostgreSQL) con Row Level Security
- **Despliegue:** Vercel
- **Control de versiones:** Git / GitHub

## Requisitos

- Python 3.10 o superior
- Git
- API key de REST Countries (gratuita, sin tarjeta — ver sección "Configuración")
- Cuenta de Supabase (gratuita)
- Conexión a internet (para consultar la API y la base de datos)

### Dependencias del proyecto

Las dependencias se instalan automáticamente con `pip install -r requirements.txt`. Entre las principales:

- `requests` → Para consumir la API de países.
- `python-dotenv` → Para manejar las variables de entorno.
- `flask` → Para el servidor web y la API interna.
- `supabase` → Cliente oficial para conectarse a Supabase.

## Instalación

```bash
git clone https://github.com/JoseSanchez23/proyecto-final-prograweb.git
cd proyecto-final-prograweb
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno necesarias

Copiar el archivo de ejemplo y completarlo con tus propios valores (nunca se sube el `.env` real a GitHub):

```bash
cp env_example .env
```

Variables requeridas (sin revelar valores reales aquí):

```
API_BASE_URL=            # URL base de REST Countries API
API_KEY=                 # API key de REST Countries
SUPABASE_URL=             # URL del proyecto de Supabase (sin /rest/v1/ al final)
SUPABASE_KEY=             # anon public key — solo lectura, usada por operaciones públicas
SUPABASE_SERVICE_KEY=     # service_role key — solo la usa el backend, para escritura
```

### Configuración de la API key de REST Countries

1. Registrarse en https://restcountries.com/sign-up y obtener una API key (free tier: 500 requests/mes, sin tarjeta).
2. Completar `API_KEY` en el `.env`.

> **Para pruebas rápidas:** puedes usar la demo key oficial, que no requiere registro: `API_KEY=rc_live_demo` (con limitaciones).

### Configuración de Supabase

1. Crear un proyecto gratuito en https://supabase.com.
2. En `Project Settings → API`, copiar el **Project URL** y las llaves **anon public** y **service_role**.
3. Completar `SUPABASE_URL`, `SUPABASE_KEY` y `SUPABASE_SERVICE_KEY` en el `.env`.

El archivo `.env` está excluido del repositorio mediante `.gitignore`. Cada integrante mantiene su propia copia local; nunca se sube a GitHub.

## Uso de Supabase

**Tabla creada:** `paises`, con las columnas `nombre`, `nombre_oficial`, `capital`, `region`, `subregion`, `poblacion`, `area_km2`, `moneda`, `idioma`, `bandera_url` y `fecha_actualizacion`.

**Qué se almacena:** cada país consultado por un usuario se guarda (o actualiza, si ya existía) automáticamente al momento de la búsqueda, funcionando como historial de consultas.

**Cómo se conecta la aplicación:** `src/database.py` inicializa un cliente de Supabase usando la `service_role key`, ya que las operaciones de guardado las realiza exclusivamente el backend (nunca el navegador del usuario).

**Medidas de seguridad aplicadas:**
- Row Level Security (RLS) activado en la tabla `paises`.
- Política de **solo lectura pública** (`SELECT`) para la `anon key`: cualquiera puede consultar el historial, pero nadie puede modificarlo usando esa key.
- No existe política de escritura para claves públicas. Las inserciones/actualizaciones (`guardar_pais`) las realiza únicamente el backend, autenticado con la `service_role key`.
- La `service_role key` nunca se expone al frontend ni se sube al repositorio; vive solo en el `.env` local y en las variables de entorno de Vercel.

## Ejecución

El proyecto tiene dos modos de ejecución: el **backend en consola** (para pruebas y desarrollo) y el **servidor web completo** (para usar la interfaz gráfica).

### 1. Backend en consola (modo básico)

```bash
python -m app.main --search "Costa Rica"
```

**Nota:** ejecutar siempre con `python -m app.main`, no `python app/main.py`. La flag `-m` agrega la raíz del proyecto a la ruta de búsqueda de módulos; sin ella, la importación `from src...` falla con `ModuleNotFoundError: No module named 'src'`.

### 2. Servidor web (modo completo con interfaz gráfica)

Este modo inicia un servidor Flask que sirve la interfaz web y la API. Es el modo recomendado.

```bash
pip install -r requirements.txt   # asegúrate de tener todo instalado
python -m app.server
```

Verás un mensaje como:
```
🌍 WorldExplorer - Servidor Web
📡 Servidor corriendo en: http://localhost:5001
```

Ve a `http://localhost:5001`, busca un país (ej. "Costa Rica"), y confirma en el panel de Supabase (`Table Editor → paises`) que la búsqueda quedó registrada.

#### Endpoints disponibles

| Endpoint | Ejemplo |
| :--- | :--- |
| Buscar país | `http://localhost:5001/api/countries/search?name=Costa%20Rica` |
| Comparar países | `http://localhost:5001/api/countries/compare?country1=Costa%20Rica&country2=Mexico` |
| Países guardados | `http://localhost:5001/api/countries/saved` |

## Despliegue en producción (Vercel)

1. Conectar el repositorio de GitHub a un nuevo proyecto en [Vercel](https://vercel.com).
2. En `Settings → Environment Variables` del proyecto en Vercel, agregar las mismas variables del `.env` (`API_BASE_URL`, `API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`).
3. El archivo `vercel.json` en la raíz del proyecto indica a Vercel cómo ejecutar la aplicación Flask como función serverless.
4. Verificar tras el despliegue que la app cargue correctamente y que las búsquedas se sigan guardando en Supabase.

## Separación de ambientes

- **Local:** usa el archivo `.env` propio de cada integrante, nunca compartido ni subido al repositorio.
- **Producción:** las mismas variables se configuran directamente en el dashboard de Vercel, de forma independiente al código fuente.

## Pruebas

```bash
python -m unittest discover tests
```

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
| `ModuleNotFoundError: No module named 'flask'` / `'supabase'` | Dependencia no instalada | Ejecutar `pip install -r requirements.txt` |
| `supabase_url is required` | `.env` no tiene `SUPABASE_URL`, está mal nombrado, o el archivo no está en la raíz | Verificar `cat .env` y que el archivo esté en la raíz del proyecto |
| `APIError: Invalid path specified in request URL` (PGRST125) | `SUPABASE_URL` incluye `/rest/v1/` al final | Dejar la URL solo hasta `.supabase.co`, sin ruta adicional |
| Import de `requests`/`dotenv`/`supabase` marcado en el editor | VS Code usando un intérprete distinto al del `venv` | `Cmd/Ctrl+Shift+P` → "Python: Select Interpreter" → seleccionar `./venv/bin/python` |
| `Address already in use` | El puerto 5001 está ocupado | Cambiar el puerto en `app/server.py` a `port=5002` |
| La API devuelve error 404 | La API key es inválida o no está configurada | Verificar el archivo `.env` o usar `API_KEY=rc_live_demo` |
| Datos guardados no aparecen en Supabase | La tabla no se refresca sola | Refrescar manualmente el `Table Editor` en Supabase |

## Documentación adicional

Para una explicación detallada de la arquitectura, el flujo de datos y las decisiones de diseño, consulta [docs/arquitectura.md](docs/arquitectura.md).
