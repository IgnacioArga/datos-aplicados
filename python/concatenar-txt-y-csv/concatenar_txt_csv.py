import pandas as pd
import os

# 1. Definir carpetas de entrada y salida
input_folder  = "ruta/a/tu/carpeta_entrada"
output_folder = "ruta/a/tu/carpeta_salida"
os.makedirs(output_folder, exist_ok=True)  # crea la carpeta de salida si no existe; si ya existe, no da error

# 2. Archivo de salida (si existe, se agregan filas; si no, se crea con encabezado)
output_file = os.path.join(output_folder, "datos_unificados.csv")

# 3. Listar archivos .txt y .csv en la carpeta de entrada
archivos = [
    f for f in os.listdir(input_folder)
    if f.endswith(".txt") or f.endswith(".csv")
]

# 4. Leer cada archivo en un DataFrame y acumularlos
dfs = []
for nombre in archivos:
    ruta = os.path.join(input_folder, nombre)
    sep = "|" if nombre.lower().endswith(".txt") else ","
    df = pd.read_csv(ruta, sep=sep, encoding="latin1")
    dfs.append(df)

# 5. Concatenar todos los DataFrames
df_total = pd.concat(dfs, ignore_index=True)

# 6. Limpiar nombres de columnas y eliminar filas completamente vacías
df_total.columns = df_total.columns.str.lower().str.strip()
df_total.dropna(how="all", inplace=True) 
# si llegaste a leer esto, contame que riesgos puede traer este dropna y que alternativas hay 

# 7. Exportar o apendear al CSV existente
if os.path.exists(output_file):
    df_total.to_csv(output_file, mode="a", header=False, index=False)
    print(f"Se han apendado {len(df_total)} filas a {os.path.basename(output_file)}")
else:
    df_total.to_csv(output_file, mode="w", header=True, index=False)
    print(f"CSV creado: {os.path.basename(output_file)} ({len(df_total)} filas)")
