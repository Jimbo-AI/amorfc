import json
import os
from fastapi import HTTPException, Query
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.functions.bot_files.bot_response import *
from app.functions.business_logic import *
router = APIRouter()


@router.get("/")
async def verify_webhook(hub_mode: str = Query(None, alias="hub.mode"),
                         hub_challenge: int = Query(None, alias="hub.challenge"),
                         hub_verify_token: str = Query(None, alias="hub.verify_token")):
    if hub_verify_token == "bWF0dGlsZGEtYm90":
        return hub_challenge
    else:
        raise HTTPException(status_code=403, detail="Error de autenticación.")


@router.post("/")
async def receive_webhook(data: dict = None):
    # wa_message = WhatsAppBusinessAccount(**data)
    # text_body = wa_message.entry[0].changes[0].value.messages[0].text.body
    # wa_id = wa_message.entry[0].changes[0].value.contacts[0].wa_id
    #
    # chat_gpt_response = generate_basic_response(text_body)
    # print(chat_gpt_response)

    try:
        json_data = json.dumps(data, indent=4)
        print("DEBUG: ", json_data)
        log_record(json_data, "webhook_log")
        data = json.loads(json_data)
        if data is not None:
            json_data = json.dumps(data, indent=4)
            print(json_data)
            type_in = data['entry'][0]['changes'][0]['field']
            if type_in == "messages":
                validate_msg = data['entry'][0]['changes'][0]['value']
                if "messages" in validate_msg:
                    phone = data['entry'][0]['changes'][0]['value']['messages'][0]['from'].replace("521", "52")
                    wa_id = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                    timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
                    name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                    message = None
                    id = None
                    type = data['entry'][0]['changes'][0]['value']['messages'][0]['type']
                    if type == 'text':
                        message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                        if phone[3:] == os.getenv("ADMIN_PHONE"):
                            if "context" in message:
                                response_id_wa = message["context"]["id"]
                                response_wa = response_admin(response_id_wa, message)
                            else:
                                response_wa = response_text(phone, "admin", "admin_message", wa_id, timestamp)
                    elif type == 'interactive':
                        type_interactive = data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['type']
                        if type_interactive == 'list_reply':
                            message = \
                            data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply']['title']
                            id = data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
                                'id']
                        if type_interactive=='button_reply':
                            message = \
                            data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply']['title']
                            id = data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply'][
                                'id']
                    elif type=='button':
                        message = data['entry'][0]['changes'][0]['value']['messages'][0]['button']['text']
                    log_record(json_data, phone)
                    if message is not None:
                        if get_email(phone) is None and (
                                '¿Cual es tu correo electrónico?' in get_last_message(phone)[0][1] or \
                                get_last_message(phone)[0][2] == 'mail'):
                            if is_valid_email(message.lower().strip()):
                                update_email(phone, message)
                                response_bot(phone, name, message, wa_id, timestamp, 'active', id)
                                # insert_message(phone, str(name), str(message), 'menu', wa_id, timestamp,
                                #                'text',
                                #                'active')
                                # text_message = payload_message_text(phone, 'Muchas gracias por tu información', False)
                                # send_message(text_message)
                                # send_message(menu_message(phone))
                            else:
                                response = 'El correo electrónico no es válido, por favor ingresa uno válido.'
                                insert_message(phone, str(name), str(message), str(response), wa_id, timestamp,
                                               'mail',
                                               'active')
                                send_message(payload_message_text(phone, response, False))
                        else:
                            response_bot(phone, name, message, wa_id, timestamp, 'active', id)
                    return JSONResponse(content={"status": "mensaje recibido"}, status_code=200)
                else:
                    return JSONResponse(content={"status": "el tipo de evento diferente a un mensaje"}, status_code=400)
            else:
                return JSONResponse(content={"status": "El tipo de evento diferente a un mensaje"}, status_code=400)
        else:
            raise HTTPException(status_code=400, detail="No data received")

    except Exception as ex:
        print("[ERROR] receive_webhook")
        print("[ERROR] ", ex)
        return JSONResponse(content={"status": "error al recibir el mensaje"}, status_code=400)
