# Automatización con SQL y alerta por Slack para detectar transacciones sospechosas

import pandas as pd
from sqlalchemy import create_engine
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ----------------------
# Configuración
# ----------------------
# String de conexión a la base de datos
DB_CONNECTION_STRING = (
    "mssql+pyodbc://<usuario>:<password>@<servidor>/<base_datos>?driver=ODBC+Driver+17+for+SQL+Server"
)

# Token de Slack (Bot User OAuth Token)
SLACK_TOKEN = "xoxb-XXXXXXXXXXXXXXXXXXXXXXXX"
SLACK_CHANNEL = "#riesgos-cumplimiento"

# ----------------------
# Funciones
# ----------------------
def obtener_transacciones_sospechosas(engine):
    query = """
    WITH historial AS (
        SELECT
            client_id,
            AVG(transaction_amount) AS promedio,
            MAX(transaction_amount) AS maximo
        FROM transactions
        WHERE transaction_date >= DATEADD(month, -6, GETDATE())
        GROUP BY client_id
    )
    SELECT
        t.client_id,
        t.transaction_id,
        t.transaction_amount
    FROM transactions t
    JOIN historial h ON t.client_id = h.client_id
    WHERE
        t.transaction_date >= DATEADD(day, -1, GETDATE())
        AND t.transaction_amount > 3 * h.promedio
        AND t.transaction_amount > 1.5 * h.maximo;
    """
    return pd.read_sql(query, engine)

def enviar_alertas_por_slack(cliente: WebClient, canal: str, df: pd.DataFrame):
    for client_id, grupo in df.groupby("client_id"):
        texto = [f"*Cliente:* {client_id}"]
        for _, fila in grupo.iterrows():
            texto.append(f"• Transacción {fila.transaction_id}: ${fila.transaction_amount:,.2f}")
        mensaje = "\n".join(texto)
        try:
            cliente.chat_postMessage(channel=canal, text=mensaje)
            print(f"Alerta enviada para cliente {client_id}")
        except SlackApiError as e:
            print(f"Error al enviar alerta para {client_id}: {e.response['error']}")

# ----------------------
# Ejecución principal
# ----------------------
if __name__ == "__main__":
    engine = create_engine(DB_CONNECTION_STRING)
    slack_client = WebClient(token=SLACK_TOKEN)

    df_alertas = obtener_transacciones_sospechosas(engine)

    if df_alertas.empty:
        print("No se encontraron transacciones sospechosas.")
    else:
        enviar_alertas_por_slack(slack_client, SLACK_CHANNEL, df_alertas)
