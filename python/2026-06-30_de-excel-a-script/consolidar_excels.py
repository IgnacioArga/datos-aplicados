"""
Consolidar varios Excel en uno solo con pandas.
Caso típico: te llegan N planillas (una por sucursal / por mes) y las tenés que pegar a mano.
Esto las une todas en segundos y deja un único archivo listo.
"""
from pathlib import Path
import pandas as pd

CARPETA = Path("entrada")        # carpeta donde caen los Excel
SALIDA  = "consolidado.xlsx"

# 1. busca todos los .xlsx de la carpeta
archivos = sorted(CARPETA.glob("*.xlsx"))

# 2. lee cada uno y le agrega de qué archivo vino (trazabilidad)
dfs = []
for f in archivos:
    df = pd.read_excel(f)
    df["origen"] = f.stem
    dfs.append(df)

# 3. los apila en una sola tabla y guarda
consolidado = pd.concat(dfs, ignore_index=True)
consolidado.to_excel(SALIDA, index=False)
print(f"{len(archivos)} archivos -> {len(consolidado)} filas en {SALIDA}")
