# Paso 0: instala las librerías necesarias con:
# pip install pandas requests

import pandas as pd
import requests
import math

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
API_KEY = 'TU_API_KEY_DE_GOOGLE_MAPS'  # <- Reemplaza con tu API Key
INPUT_CSV = 'direcciones.csv'          # Nombre de tu archivo de direcciones
OUTPUT_CSV = 'distancias.csv'          # Archivo donde guardaremos resultados

# -----------------------------
# Función para geocodificar una dirección
# -----------------------------
def geocode(address):
    """
    Llama a la API de Google Maps Geocoding
    y devuelve (latitud, longitud) para una cadena de dirección.
    """
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': API_KEY
    }
    response = requests.get(url, params=params).json()
    location = response['results'][0]['geometry']['location']
    return location['lat'], location['lng']

# -----------------------------
# 1. Leemos el CSV con todas las direcciones
# -----------------------------
df = pd.read_csv(INPUT_CSV)  # Debe haber una columna llamada "address"

# -----------------------------
# 2. Geolocalizamos cada dirección
# -----------------------------
latitudes = []
longitudes = []
for direccion in df['address']:
    lat, lng = geocode(direccion)
    latitudes.append(lat)
    longitudes.append(lng)

df['lat'] = latitudes
df['lng'] = longitudes

# -----------------------------
# 3. Geolocalizamos también casa y trabajo
# -----------------------------
mi_casa = 'Calle Falsa 123, Ciudad, País'
mi_trabajo = 'Avenida Siempre Viva 742, Ciudad, País'

casa_lat, casa_lng = geocode(mi_casa)
trabajo_lat, trabajo_lng = geocode(mi_trabajo)

# -----------------------------
# 4-5. Calculamos distancias con Pitágoras y convertimos a km
# -----------------------------
# Aproximación: 1 grado ≃ 111,32 km
KM_POR_GRADO = 111.32

# Función auxiliar para distancia euclidiana en km
def distancia_km(lat1, lng1, lat2, lng2):
    dlat = lat1 - lat2
    dlng = lng1 - lng2
    # distancia en grados
    dist_grados = math.sqrt(dlat**2 + dlng**2)
    # convertimos a km
    return dist_grados * KM_POR_GRADO

# -----------------------------
# 6. Creamos dos columnas muy claras
# -----------------------------
df['distancia_a_casa_km'] = df.apply(
    lambda row: distancia_km(row['lat'], row['lng'], casa_lat, casa_lng),
    axis=1
)

df['distancia_al_trabajo_km'] = df.apply(
    lambda row: distancia_km(row['lat'], row['lng'], trabajo_lat, trabajo_lng),
    axis=1
)

# -----------------------------
# 7. Guardamos y mostramos el resultado
# -----------------------------
df_resultado = df[['address', 'distancia_a_casa_km', 'distancia_al_trabajo_km']]
df_resultado.to_csv(OUTPUT_CSV, index=False)
