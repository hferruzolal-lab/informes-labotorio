import os
import json
import html
import urllib.request
import urllib.error


def enviar_correo_brevo(destinatario, asunto, mensaje):

    api_key = os.environ.get("BREVO_API_KEY", "")
    sender_email = os.environ.get("BREVO_SENDER_EMAIL", "")
    sender_name = os.environ.get("BREVO_SENDER_NAME", "Reporte de Daños")

    if not api_key:
        raise Exception("Falta BREVO_API_KEY en Render.")

    if not sender_email:
        raise Exception("Falta BREVO_SENDER_EMAIL en Render.")

    datos = {
        "sender": {
            "name": sender_name,
            "email": sender_email
        },
        "to": [
            {
                "email": destinatario
            }
        ],
        "subject": asunto,
        "textContent": mensaje,
        "htmlContent": f"<pre>{html.escape(mensaje)}</pre>"
    }

    request = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(datos).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8")

    except urllib.error.HTTPError as error:
        detalle = error.read().decode("utf-8")
        raise Exception(f"Error Brevo {error.code}: {detalle}")

    except Exception as error:
        raise Exception(f"Error enviando correo con Brevo: {error}")