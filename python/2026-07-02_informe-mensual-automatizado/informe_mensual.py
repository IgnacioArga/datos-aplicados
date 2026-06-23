"""
Caso anonimizado: informe mensual que antes se armaba a mano cruzando varias planillas.
El script: (1) junta todas las fuentes, (2) limpia lo basico, (3) arma el resumen por
categoria y (4) exporta el Excel final. Lo que tardaba una manana, queda en segundos.
(Datos y nombres son de ejemplo; el patron es el real.)
"""
from pathlib import Path
import pandas as pd

ENTRADA = Path("fuentes")     # las N planillas crudas del mes
SALIDA  = "informe_mensual.xlsx"

# 1. juntar todas las fuentes
dfs = []
for f in sorted(ENTRADA.glob("*.xlsx")):
    dfs.append(pd.read_excel(f))
datos = pd.concat(dfs, ignore_index=True)

# 2. limpieza basica (lo que come el 80% del tiempo si se hace a mano)
datos.columns = [c.strip().lower() for c in datos.columns]        # normalizar headers
datos["categoria"] = datos["categoria"].str.strip().str.title()  # "  ropa " -> "Ropa"
datos["importe"] = pd.to_numeric(datos["importe"], errors="coerce")
datos = datos.dropna(subset=["importe"])                          # filas rotas fuera

# 3. resumen por categoria
resumen = (datos.groupby("categoria", as_index=False)
                .agg(operaciones=("importe", "size"),
                     total=("importe", "sum"))
                .sort_values("total", ascending=False))
resumen["pct"] = (resumen["total"] / resumen["total"].sum() * 100).round(1)

# 4. exportar
with pd.ExcelWriter(SALIDA) as xls:
    datos.to_excel(xls, sheet_name="detalle", index=False)
    resumen.to_excel(xls, sheet_name="resumen", index=False)

print(f"{len(datos)} filas limpias | {len(resumen)} categorias -> {SALIDA}")
print(resumen.to_string(index=False))
