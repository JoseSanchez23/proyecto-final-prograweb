# Arquitectura del proyecto

## Visión general

El proyecto sigue una separación en capas, donde cada módulo tiene una única responsabilidad. Esta separación permite modificar la fuente de datos (la API) o el destino de almacenamiento (la base de datos) sin afectar al resto del código.

```
┌─────────────────────────┐
│  REST Countries API v5  │   fuente externa de datos
└────────────┬─────────────┘
             │ HTTP GET (Authorization: Bearer)
             ▼
┌─────────────────────────┐
│   src/api_client.py      │   capa de conexión
│   - get_all_countries()  │   - arma la URL y los headers
│   - get_country_by_name()│   - maneja errores de red y timeouts
│   - get_countries_by_region() │ - valida respuestas vacías
└────────────┬─────────────┘
             │ lista de diccionarios (JSON crudo)
             ▼
┌─────────────────────────┐
│   src/models.py           │   capa de modelo
│   - class Country          │   - define la forma de los datos que
│   - from_api_response()    │     usa el resto de la aplicación
└────────────┬─────────────┘
             │ objeto Country
             ▼
┌─────────────────────────┐
│   src/services.py          │   capa de lógica de negocio
│   - buscar_pais()           │   - combina api_client + models
│   - paises_por_region()     │   - punto único de acceso para app/
└────────────┬─────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
┌───────────┐  ┌──────────────────┐
│ app/main.py│  │ src/database.py    │
│ (presentación)│ (persistencia)   │
└───────────┘  └──────────────────┘
                       │
                       ▼
                  paises.db (SQLite)
```

## Responsabilidad de cada módulo

### `src/api_client.py`
El único punto de contacto con la API externa. No posee conocimiento sobre cómo se van a usar los datos después; solo sabe hacer la petición HTTP, adjuntar la API key, y devolver una lista de objetos o `None` si algo llegase a fallar (error de red, timeout o bien una respuesta vacía).

### `src/models.py`
Define la clase `Country`, que representa un país con los campos relevantes para la aplicación (nombre, capital, población, moneda, idioma, etc.). El método `from_api_response()` es el único lugar del código que conoce la estructura específica del JSON que devuelve la API v5 (campos anidados como `names.common`, `capitals[0].name`, `area.kilometers`). En caso de que la API vuelve a cambiar su formato, solo este método necesita ajustarse.

### `src/database.py`
Integra toda la interacción con SQLite, desde la creación de la tabla, inserción/actualización de países (usando `ON CONFLICT` para evitar duplicados) hasta la lectura de los registros guardados.

### `src/services.py`
Capa intermedia que combina `api_client` y `models`: pide los datos crudos a la API y los convierte en objetos `Country` listos para usar. Es el módulo que el resto de la aplicación (por ejemplo, `app/main.py`, o a futuro una interfaz web) debería llamar, en lugar de acceder directamente a `api_client` o `models`.

### `app/main.py`
Punto de entrada del programa. Orquesta el flujo completo: busca un país, lo muestra, lo guarda en la base de datos y lista lo almacenado hasta el momento.

## Decisiones de diseño

- **Separación API / modelo / persistencia**: permite testear cada capa de forma independiente (por ejemplo, probar `models.py` con un JSON de ejemplo sin necesidad de conexión a internet).
- **Manejo de errores en `api_client.py`**: toda excepción de red se captura ahí; el resto del código recibe `None` en caso de fallo y decide qué hacer, en lugar de propagar excepciones no controladas.
- **Credenciales fuera del código**: la API key se lee desde variables de entorno (`.env`, excluido del control de versiones), nunca se escribe directamente en el código fuente.
- **`ON CONFLICT` en SQLite**: evita registros duplicados (si se consulta el mismo país más de una vez); actualiza los datos existentes en lugar de crear una fila nueva.

## Posibles extensiones futuras

- Reemplazar `app/main.py` por una interfaz web (Flask/FastAPI) que exponga endpoints propios sobre los datos ya almacenados.
- Agregar una capa de caché para reducir las llamadas a la API dentro del límite del free tier (500 requests/mes).
- Incorporar tests automatizados sobre `services.py` usando datos de ejemplo, sin depender de la API real.