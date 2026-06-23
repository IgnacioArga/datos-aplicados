-- LUNES: INNER JOIN vs LEFT JOIN -- analogia del asado
-- Tabla 1: invitados (los que dijeron que venian)
-- Tabla 2: confirmaciones (los que confirmaron que traen algo)

CREATE TABLE invitados (
  id      INTEGER PRIMARY KEY,
  nombre  TEXT
);

CREATE TABLE confirmados (
  invitado_id INTEGER,
  trae        TEXT
);

INSERT INTO invitados (id, nombre) VALUES
  (1, 'Sofia'),
  (2, 'Martin'),
  (3, 'Lucia'),
  (4, 'Diego');

-- Solo algunos confirmaron que traen algo
INSERT INTO confirmados (invitado_id, trae) VALUES
  (1, 'Provoleta'),
  (2, 'Vino'),
  (3, 'Ensalada');
-- Diego (id 4) NO confirmo

.print '==== INNER JOIN (solo los que confirmaron: cruce que existe en AMBAS listas) ===='
.mode column
.headers on
SELECT i.nombre, c.trae
FROM invitados i
INNER JOIN confirmados c ON c.invitado_id = i.id;

.print ''
.print '==== LEFT JOIN (TODOS los invitados; los que no confirmaron quedan en NULL) ===='
SELECT i.nombre, c.trae
FROM invitados i
LEFT JOIN confirmados c ON c.invitado_id = i.id;
