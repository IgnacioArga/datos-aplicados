# Detección de transacciones sospechosas

Patrón de monitoreo: una query SQL marca transacciones que superan ciertos umbrales sobre el historial del cliente, y manda una alerta automática a Slack. Pensado para riesgo/cumplimiento.

**Requisitos:** `pandas`, `sqlalchemy`, `slack_sdk`. Configurá el string de conexión y el token de Slack (vienen como placeholders).
**Cómo correr:** `python deteccion_transacciones.py`

_Ejemplo de la librería (no atado a un post puntual)._
