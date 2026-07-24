# Entrega 1 - Backend y procesamiento

## Objetivo

Desarrollar el backend inicial del World Explorer como primera entrega: conexión a la API externa, procesamiento de datos, almacenamiento local y documentación del flujo.

## Qué se hizo

1. Se revisó el estado actual del código en `src/api_client.py`, `src/models.py`, `src/services.py` y `src/database.py`.
2. Se mejoró la capa de conexión con la API para que funcione con REST Countries API v5 y use la `API_KEY` desde variables de entorno.
3. Se reforzó el procesamiento de la respuesta de la API en `Country.from_api_response()`, para manejar campos opcionales y normalizar los datos.
4. Se amplió la lógica del servicio para permitir búsquedas de país por nombre y listado por región.
5. Se mejoró la persistencia SQLite para ordenar los países guardados y agregar una consulta por país guardado.
6. Se dejó un punto de entrada más claro en `app/main.py`, con ejecución de ejemplo y formato educativo para jóvenes.
7. Se agregó un test de unidad inicial para comprobar el parseo de la respuesta de la API.

## Estructura del backend

- `src/api_client.py`: conexión HTTP con la API externa, manejo de errores, lectura de JSON y validación de la respuesta.
- `src/models.py`: modelo `Country` que transforma el JSON crudo en datos listos para la aplicación.
- `src/services.py`: funciones de negocio para buscar países y obtener listas en formato `Country`.
- `src/database.py`: persistencia en SQLite, creación de tabla, inserción/actualización y consultas.
- `app/main.py`: ejemplo de uso y demostración de búsqueda, guardado y listado.

## Cómo probarlo

1. Copiar `.env.example` a `.env` y completar `API_KEY`.
2. Ejecutar `python -m app.main "Costa Rica"`.
3. Verificar que el país se imprime y se guarda en `paises.db`.
4. Ejecutar pruebas con:

```bash
python -m unittest discover -s tests
```

## Notas para la primera entrega

- Esta implementación es un prototipo inicial. Para futuras entregas se recomienda:
  - agregar una interfaz web (Flask/FastAPI) para consultas desde el frontend.
  - incluir caché de consultas para respetar el límite de requests del plan gratuito.
  - añadir más tests sobre los servicios y la persistencia.
  - definir claramente los campos que se mostrarán en el comparador de países (población, área, capital, moneda, idioma, bandera, densidad, región, capital, etc.).

## Próximos pasos

- Definir la API interna del backend para que el frontend pueda solicitar comparaciones y búsquedas.
- Crear endpoints REST que expongan datos ya procesados y almacenados.
- Construir la interfaz educativa para jóvenes con explicaciones amigables y datos visuales.
