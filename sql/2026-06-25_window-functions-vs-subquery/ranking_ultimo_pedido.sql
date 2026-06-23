-- JUEVES: benchmark "antes vs despues"
-- Patron: quedarse con el ULTIMO pedido de cada cliente (una fila por cliente).
-- ANTES: subquery correlacionada (se re-ejecuta una vez por fila -> O(n^2))
-- DESPUES: window function ROW_NUMBER() = 1 (una sola pasada -> O(n log n))
-- Reproducible en SQLite 3.25+ (soporta window functions). QUALIFY NO existe en
-- SQLite: se muestra mas abajo como variante para Redshift/Snowflake/BigQuery.

.timer on

-- ~50.000 pedidos de ~5.000 clientes
CREATE TABLE pedidos (
  id          INTEGER PRIMARY KEY,
  cliente_id  INTEGER,
  fecha       TEXT,
  monto       REAL
);

WITH RECURSIVE seq(n) AS (
  SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n < 50000
)
INSERT INTO pedidos (id, cliente_id, fecha, monto)
SELECT n,
       (n % 5000) + 1,
       date('2025-01-01', '+' || (n % 365) || ' days'),
       round(abs(random() % 100000) / 100.0, 2)
FROM seq;

.print '######## ANTES: subquery correlacionada (sin indice) ########'
-- Por cada fila pregunta "¿es esta la fila mas nueva de su cliente?".
-- La subquery se re-ejecuta una vez por fila y recorre la tabla entera.
SELECT count(*) AS filas, round(sum(monto), 2) AS control
FROM pedidos p
WHERE p.id = (
  SELECT p2.id
  FROM pedidos p2
  WHERE p2.cliente_id = p.cliente_id
  ORDER BY p2.fecha DESC, p2.id DESC
  LIMIT 1
);

.print ''
.print '######## DESPUES: window function ROW_NUMBER() = 1 (una sola pasada) ########'
-- Numera los pedidos de cada cliente del mas nuevo al mas viejo y se queda con el 1.
-- Ojo: row_number = 1 NO se puede filtrar en el WHERE -> se calcula en un CTE/subquery.
SELECT count(*) AS filas, round(sum(monto), 2) AS control
FROM (
  SELECT p.*,
         ROW_NUMBER() OVER (
           PARTITION BY p.cliente_id
           ORDER BY p.fecha DESC, p.id DESC
         ) AS rn
  FROM pedidos p
)
WHERE rn = 1;

.print ''
.print '######## EXTRA: misma idea ANTES PERO con indice (cliente_id, fecha) ########'
-- Si te toca quedarte con la subquery, la palanca es el indice correcto:
-- el motor va directo a la fila en vez de escanear todo.
CREATE INDEX idx_pedidos_cli_fecha ON pedidos(cliente_id, fecha DESC, id DESC);
SELECT count(*) AS filas, round(sum(monto), 2) AS control
FROM pedidos p
WHERE p.id = (
  SELECT p2.id
  FROM pedidos p2
  WHERE p2.cliente_id = p.cliente_id
  ORDER BY p2.fecha DESC, p2.id DESC
  LIMIT 1
);

-- ######## VARIANTE QUALIFY (Redshift / Snowflake / BigQuery) ########
-- Estos motores permiten filtrar la window function en la misma query, sin CTE.
-- (No corre en SQLite; queda como referencia.)
--
--   SELECT *
--   FROM pedidos
--   QUALIFY ROW_NUMBER() OVER (
--             PARTITION BY cliente_id
--             ORDER BY fecha DESC, id DESC
--           ) = 1;
