import openai
import pandas as pd
import json

# 1. Configuración de la API
openai.api_key = "sk-tu-clave-aquí"

# 2. Leer CSV
# El archivo 'transacciones.csv' debe tener columnas: fecha, monto, descripcion
#df = pd.read_csv("transacciones.csv")
df = pd.DataFrame([
    {"fecha": "2025-05-28", "monto": 15.20, "descripcion": "STARBUCKS 123"},
    {"fecha": "2025-05-29", "monto": 120.00, "descripcion": "AMAZON MKTPLACE"},
    {"fecha": "2025-05-30", "monto": 9.50, "descripcion": "METRO MADRID"}
])


# 3. Preparar y enviar el prompt
# Serializamos las transacciones a JSON
payload = json.dumps(df.to_dict(orient="records"), ensure_ascii=False)

resp = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un experto en finanzas personales."},
        {"role": "user", "content":
            "Categoriza estas transacciones en: Alimentación, Transporte, Compras, "
            "Suscripciones, Ocio, Otros.\n\n" + payload
        }
    ]
)

# 4. Parsear la respuesta asumiendo siempre viñetas “- DESCRIPCIÓN: CATEGORÍA”
texto = resp.choices[0].message.content.strip()
mapping = {}
for línea in texto.splitlines():
    if línea.startswith("- "):
        desc, cat = línea[2:].split(":", 1)
        mapping[desc.strip()] = cat.strip()

# 5. Asignar categorías al DataFrame
df["categoria"] = df["descripcion"].map(mapping).fillna("Otros")

# 6. Mostrar o guardar resultado
print(df)
# df.to_csv("transacciones_categorizadas.csv", index=False)