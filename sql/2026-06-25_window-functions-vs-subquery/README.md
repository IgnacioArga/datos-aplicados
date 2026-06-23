# Window function vs subquery

Quedarte con el último pedido de cada cliente. Compara el **antes** (subquery correlacionada, se re-ejecuta por fila → O(n²)) contra el **después** (`ROW_NUMBER() = 1`, una sola pasada). Incluye variante con `QUALIFY` para Redshift/Snowflake/BigQuery.

**Requisitos:** SQLite 3.25+ (soporta window functions).
**Cómo correr:** `sqlite3 < ranking_ultimo_pedido.sql`

🔗 Post de LinkedIn: _pendiente de publicación._
