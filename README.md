# datos-aplicados

Código y recursos de mis publicaciones sobre **análisis de datos aplicado a decisiones de negocio**: SQL, Python, visualización e IA. Ejemplos reproducibles, pensados para que los puedas correr y adaptar.

Por **Ignacio Argañaraz** — Senior Data Scientist.
🔗 LinkedIn: https://www.linkedin.com/in/TU-PERFIL  _(reemplazar por tu URL real)_

## Cómo está organizado

Carpetas por temática: `sql/`, `python/`, `viz/`, `ia/`.
- Los recursos que acompañan a un post viven en `<temática>/<fecha>_<tema>/` y tienen su propio README con el contexto y el link al post.
- Los ejemplos de la librería (no atados a un post puntual) van por temática, sin fecha.

## Índice

### SQL
- [INNER JOIN vs LEFT JOIN](sql/2026-06-22_joins-inner-vs-left/) — la diferencia explicada con la analogía del asado.
- [Window function vs subquery](sql/2026-06-25_window-functions-vs-subquery/) — quedarte con el último pedido de cada cliente, de O(n²) a una sola pasada.

### Python
- [De Excel a script](python/2026-06-30_de-excel-a-script/) — consolidar N planillas en una, en segundos.
- [pandas vs polars](python/2026-07-01_pandas-vs-polars/) — benchmark de un `groupby` a distintos tamaños.
- [Informe mensual automatizado](python/2026-07-02_informe-mensual-automatizado/) — caso anonimizado: lo que tardaba una mañana, en segundos.
- [Concatenar TXT y CSV](python/concatenar-txt-y-csv/) — unir archivos mixtos en una sola tabla.
- [Detección de transacciones sospechosas](python/deteccion-de-transacciones-sospechosas/) — patrón SQL + alerta automática a Slack.
- [Geolocalización con Google Maps](python/geolocalizacion-con-google-maps/) — geocodificar direcciones y calcular distancias.
- [Scraping con Selenium](python/scraping-con-selenium/) — click y captura de un dato en una web.

### Visualización
- [Antes y después en gráficos](viz/2026-07-07_antes-y-despues-en-graficos/) — malas prácticas (eje truncado, torta de 8 porciones) vs su versión correcta.

### IA
- [Categorizar transacciones con OpenAI](ia/categorizar-transacciones-con-openai/) — clasificar gastos con un LLM.

## Licencia
[MIT](LICENSE) — usá el código libremente.
