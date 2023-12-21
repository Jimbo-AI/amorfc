'''
Nombre del Proyecto: Amor FC Instagram Messenger

Archivo: instagram_messenger.py

Fecha de Creación: 19 de diciembre de 2023

Última Modificación: 21 de diciembre de 2023

Descripción:

    Derechos de Autor © 2023 Jimbo. Todos los derechos reservados.
 
Licencia:
    
'''

from fastapi import FastAPI, Request, status, HTTPException
import requests
import re

app = FastAPI()

#Token de acceso a la página / ID de la página
PAGE_ACCESS_TOKEN = "token_de_acceso_a_la_página"
PAGE_ID = "id_de_la_página"

@app.post("/webhook")
async def post_webhook(request: Request):
    body = await request.json()
    # Procesa los mensajes que recibe la API
    for entry in body.get("entry", []):
        for messaging in entry.get("messaging", []):
            sender_psid = messaging.get("sender", {}).get("id")
            message_text = messaging.get("message", {}).get("text")

            if message_text:
                # Llama a la función que contiene los saludos
                response_text = handle_greetings(message_text)
                if response_text:
                    # Llama a la función para enviar una respuesta
                    await send_message(sender_psid, response_text)

    # Responde con 200 OK dentro de 20 segundos para evitar reintentos.
    return {"message": "EVENT_RECEIVED"}

def handle_greetings(message_text: str) -> str:
    # Se normaliza el mensaje a minúsculas para una mejor coincidencia
    message_text = message_text.lower()

    # Lista de saludos
    greetings = {
        "hola": "¡Hey! ¿Qué onda? 😎 ¿cómo puedo ayudarte hoy?",
        "qué onda": "¡Aquí estamos! Dime, ¿cómo puedo ayudarte hoy?",
        "hola!": "¡Hola! ¿cómo puedo ayudarte hoy? 😎",
        "hey": "¡Hey! ¿En qué puedo echarte una mano hoy? 👋",
        "qué tal": "Que tal, ¿cómo puedo ayudarte hoy?",
        "buenas": "¡Buenas! Dime, ¿cómo puedo asistirte? 🚀",
    }

    # Revisa coincidencias con el mensaje
    for greeting, response in greetings.items():
        if re.search(r"\b" + re.escape(greeting) + r"\b", message_text):
            return response

    return None

async def send_message(sender_psid: str, response_text: str):
    # Define la solicitud POST para enviar la respuesta
    request_body = {
        "recipient": {
            "id": sender_psid
        },
        "message": {
            "text": response_text
        }
    }

    # Envia solicitud a la API de Messenger
    response = requests.post(
        f"https://graph.facebook.com/v18.0/{PAGE_ID}/messages",
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=request_body
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"message_id": response.json()["message_id"]}
