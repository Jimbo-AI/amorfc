import json
import os
import requests
import logging


def payload_message_text(phone, message, preview_url):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{phone}",
        "type": "text",
        "text": {
            "preview_url": f"{preview_url}",
            "body": f"{message}"
        }
    }, indent=4)
    print(payload)
    return payload
def payload_message_button(phone, message, buttons_in):
    element_count = len(buttons_in)
    if element_count > 3:
        raise Exception("El número máximo de botones es 3")
    elif element_count < 1:
        raise Exception("El número mínimo de botones es 1")
    else:
        buttons = []
        for item in buttons_in:
            button = {
                "type": "reply",
                "reply": {
                    "id": item["id"],
                    "title": item["title"]
                }
            }
            buttons.append(button)

        result = {
            "buttons": buttons
        }

    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{phone}",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": f"{message}"
            },
            "action": result
        }
    }, indent=4)
    print(payload)
    return payload
def payload_message_list(phone, body, title, elements):
    element_count = len(elements)
    rows = []
    for item in elements:
        row = {
            "id": item["id"],
            "title": item["title"]
        }
        rows.append(row)

    result = {
        "rows": rows
    }
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{phone}",
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": f"{body}",
            },
            "action": {
                "button": f"{title}",
                "sections": [
                    {
                        "title": "Selecciona una opción",
                        "rows": result["rows"]
                    }
                ]
            }
        }

    }, indent=4)
    print(payload)
    return payload
def send_message(payload):
    try:
        token = os.environ.get("TOKEN_WA")
        url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.content)
        return response.status_code

    except Exception as ex:
        print("[ERROR] send_response")
        print("[ERROR] ", ex)
        logging.error("send_response")
        logging.error(ex)

    # if __name__ == "__main__":
#     payload_message_button("573015555555", "Hola",
#                            [{"id": "confirm", "title": "✅ Confirmar"}, {"id": "no_confirm", "title": "❌ Cancelar"}])
#     payload_message_list("573015555555", "Hola", "Confirmar",
#                      [{"id": "confirm", "title": "✅ Confirmar"}, {"id": "no_confirm", "title": "❌ Cancelar"}])
