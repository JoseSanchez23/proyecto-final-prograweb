# Arquitectura de WorldExplorer

## Visión general

El proyecto sigue una separación en capas, donde cada módulo tiene una única responsabilidad. Esta separación permitió cambiar el destino de almacenamiento (de SQLite local a Supabase en la nube) sin tener que modificar la capa de conexión a la API ni la capa de modelo de datos.

La aplicación es una app web completa: un backend Flask sirve tanto la interfaz (HTML/CSS/JS) como una API interna en JSON, y persiste los datos consultados en una base de datos PostgreSQL administrada por Supabase.

```
┌─────────────────────────┐
│ REST Countries API v5   │  fuente externa de datos
└────────────┬─────────────┘
             │ HTTP GET (Authorization: Bearer)
             ▼
┌─────────────────────────┐
│ src/api_client.py       │  capa de conexión
│ - get_all_countries()   │  - arma la URL y los headers
│ - get_country_by_name() │  - maneja errores de red y timeouts
│ - get_countries_by_region() │ - valida respuestas vacías
└────────────┬─────────────┘
             │ lista de diccionarios (JSON crudo)
             ▼
┌─────────────────────────┐
│ src/models.py           │  capa de modelo
│ - class Country         │  - define la forma de los datos que
│ - from_api_response()   │    usa el resto de la aplicación
└────────────┬─────────────┘
             │ objeto Country
             ▼
┌─────────────────────────┐
│ src/services.py         │  capa de lógica de negocio
│ - buscar_pais()         │  - combina api_client + models
│ - buscar_paises_por_region() │ - guarda cada consulta llamando
│ - comparar_paises()     │    a database.guardar_pais()
└────────────┬─────────────┘
             │
      ┌──────┴───────┐
      ▼               ▼
┌───────────┐   ┌──────────────────┐
│ app/main.py│   │ app/server.py    │
│ (consola) │   │ (servidor Flask) │
└───────────┘   └────────┬──────────┘
                          │ sirve templates/ y static/,
                          │ expone /api/countries/*
                          ▼
                 ┌──────────────────┐
                 │ src/database.py  │  capa de persistencia
                 └────────┬──────────┘
                          │ cliente Supabase (service_role key)
                          ▼
                 ┌──────────────────┐
                 │ Supabase          │
                 │ tabla `paises`    │
                 │ RLS habilitado    │
                 └──────────────────┘
```

## Responsabilidad de cada módulo

### `src/api_client.py`
El único punto de contacto con la API externa. No posee conocimiento sobre cómo se van a usar los datos después; solo sabe hacer la petición HTTP, adjuntar la API key, y devolver una lista de objetos o `None` si algo llegase a fallar (error de red, timeout o bien una respuesta vacía).

### `src/models.py`
Define la clase `Country`, que representa un país con los campos relevantes para la aplicación (nombre, capital, población, moneda, idioma, etc.). El método `from_api_response()` es el único lugar del código que conoce la estructura específica del JSON que devuelve la API v5 (campos anidados como `names.common`, `capitals[0].name`, `currencies[0].name`, `area.kilometers`). En caso de que la API vuelva a cambiar su formato, solo este método necesita ajustarse.

> Nota de mantenimiento: el campo `currencies` de la API v5 llega como **lista** de objetos, no como diccionario. `from_api_response()` maneja ambos casos por compatibilidad, pero el caso real observado en producción es siempre lista.

### `src/database.py`
Integra toda la interacción con **Supabase** (antes SQLite): inserción/actualización de países mediante `upsert` sobre la columna `nombre` (evita duplicados, actualiza si ya existe), y lectura de los registros guardados. Usa la `service_role key` para autenticarse, ya que corre exclusivamente en el backend.

### `src/services.py`
Capa intermedia que combina `api_client`, `models` y `database`: pide los datos crudos a la API, los convierte en objetos `Country`, y guarda cada país consultado mediante `guardar_pais()`. Es el módulo que el resto de la aplicación (`app/main.py`, `app/server.py`) llama, en lugar de acceder directamente a `api_client`, `models` o `database`.

### `app/main.py`
Punto de entrada del modo consola. Orquesta el flujo completo: busca un país, lo muestra, lo guarda en la base de datos y lista lo almacenado hasta el momento.

### `app/server.py`
Punto de entrada del modo web. Levanta un servidor Flask que:
- Sirve `templates/index.html` y los archivos estáticos (`static/css`, `static/js`) en `/`.
- Expone una API interna en JSON: `/api/countries/search`, `/api/countries/compare`, `/api/countries/saved`.
- Internamente reutiliza `src/services.py` para toda la lógica, sin duplicar código del modo consola.

## Persistencia: de SQLite a Supabase

La versión inicial del proyecto guardaba los datos en un archivo SQLite local (`paises.db`). Este enfoque dejó de ser viable al preparar la aplicación para producción en Vercel, porque:

- Vercel ejecuta el backend como funciones **serverless**: cada invocación puede correr en una instancia distinta y desechable.
- El sistema de archivos de esas instancias no persiste entre requests ni entre despliegues.
- Un archivo `.db` escrito en una instancia no estaría disponible en la siguiente petición.

Por eso se migró la capa de persistencia a **Supabase** (PostgreSQL administrado, accesible por red desde cualquier instancia). El resto de la arquitectura no tuvo que cambiar: `database.py` sigue exponiendo las mismas funciones (`guardar_pais`, `obtener_pais_guardado`, `listar_paises_guardados`), por lo que `services.py`, `app/main.py` y `app/server.py` no requirieron ninguna modificación.

## Seguridad de la base de datos

- **Row Level Security (RLS)** activado en la tabla `paises`.
- Política de **solo lectura** (`SELECT`) para la `anon key`, que es pública y podría llegar a exponerse en el navegador.
- **Ninguna política de escritura** para la `anon key`: insertar o actualizar solo es posible con la `service_role key`.
- La `service_role key` se usa únicamente desde `src/database.py`, en el backend, y se mantiene fuera del control de versiones (variables de entorno locales y en Vercel).

Este diseño limita el impacto de una eventual filtración de la `anon key`: en el peor caso, permitiría solo lectura de datos que de por sí son públicos en la aplicación, nunca escritura o borrado.

## Decisiones de diseño

- **Separación API / modelo / persistencia / presentación**: permite testear cada capa de forma independiente (por ejemplo, probar `models.py` con un JSON de ejemplo sin necesidad de conexión a internet), y permitió cambiar de SQLite a Supabase tocando un solo archivo.
- **Manejo de errores en `api_client.py`**: toda excepción de red se captura ahí; el resto del código recibe `None` en caso de fallo y decide qué hacer, en lugar de propagar excepciones no controladas.
- **Credenciales fuera del código**: tanto la API key de REST Countries como las llaves de Supabase se leen desde variables de entorno (`.env` local / variables de entorno de Vercel en producción), nunca se escriben directamente en el código fuente.
- **`upsert` en Supabase**: evita registros duplicados (si se consulta el mismo país más de una vez); actualiza los datos existentes en lugar de crear una fila nueva, igual que el `ON CONFLICT` que se usaba antes en SQLite.
- **Doble modo de ejecución (consola / web)**: se mantuvo `app/main.py` como modo de prueba rápida sin depender de un navegador, útil para debugging, mientras `app/server.py` es el modo de uso real de la aplicación.

## Despliegue en producción

La aplicación se despliega en **Vercel**, que ejecuta `app/server.py` como una función serverless (configurado en `vercel.json` en la raíz del repositorio). Las variables de entorno (API key, credenciales de Supabase) se configuran en el dashboard de Vercel, de forma separada al código fuente y al ambiente local.

## Posibles extensiones futuras

- Agregar una capa de caché para reducir las llamadas a la API dentro del límite del free tier (500 requests/mes).
- Incorporar tests automatizados sobre `services.py` y `database.py` usando datos de ejemplo, sin depender de la API real ni de una conexión activa a Supabase.
- Agregar autenticación de usuarios (Supabase Auth) si se quisiera personalizar el historial por persona en vez de ser compartido.