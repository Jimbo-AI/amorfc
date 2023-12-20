import os
from app.functions.whatsapp_messages import *
from app.functions.business_logic import *
from app.functions.config import connect_db
from exchangelib import DELEGATE, Account, Credentials, HTMLBody, UTC_NOW, Account, Credentials, Configuration
from exchangelib.items import MeetingRequest, CalendarItem
from unidecode import unidecode
from datetime import datetime, timedelta
import logging
import pytz

from app.ai.chat import chat_with_docs, web_data_loader, get_db
from app.ai.documents_loader import (
    text_data_loader,
    web_data_loader,
    pdf_data_loader,
    web_data_xml_sitemap_loader,
)

docs = []
# web = web_data_loader(url='https://gruporefrigerante.com')
# docs.extend(web)
# sitemap = web_data_xml_sitemap_loader(url='https://gruporefrigerante.com/sitemap.xml')
# docs.extend(sitemap)
txt = text_data_loader(path='app/documents/into_coparmex_evento.txt')
docs.extend(txt)
# pdf = pdf_data_loader(docuemnt_path='app/documents/grupo_refrigerantes.pdf')
# docs.extend(pdf)
db = get_db(docs=docs)


def saludo(phone):
    try:
        if get_name(phone) is None:
            text_init = '👋 ¡Hola! \n' \
                        '✨ Desde Coparmex, queremos expresarte nuestro más sincero agradecimiento por unirte a nosotros en este Desayuno informativo con Denise Dresser. Quien nos hablará sobre "¿Y yo qué puedo hacer? 10 Propuestas Ciudadanas para Cambiar a México".\n' \
                        '💬 ¡Yo soy Copi el asistente virtual del evento y estoy listo para contestar cualquier pregunta que tengas acerca del desayuno informativo y de sus patrocinadores! \n' \
                        'Pregúntame lo que quieras, estaré feliz de hablar contigo. \n'
            payload_out = payload_message_text(phone, text_init, False)
            # response = '¿Cual es tu nombre?'
            # payload_out = payload_message_text(phone, response, False)
            response_out = {'payload_out': payload_out, 'type': 'saludo'}
            return response_out
        else:
            if get_email(phone) is None:
                response = 'Hola ' + get_name(phone) + ', ¿Cual es tu correo electrónico?'
                payload_out = payload_message_text(phone, response, False)
                response_out = {'payload_out': payload_out, 'type': 'email'}
                return response_out
            else:
                name = get_name(phone)
                send_message(payload_message_text(phone, 'Que tal, ' + name, False))
                response = '¿En que te podemos ayudar?'
                payload_out = response
                response_out = {'payload_out': payload_out, 'type': 'menu'}
                return response_out
    except Exception as ex:
        print(ex)
        return "Error"


def nombre(phone, message_in):
    try:
        name = extract_name(message_in)
        update_name(phone, name)
        if get_email(phone) is None:
            response = 'Hola ' + name + ', ¿Cual es tu correo electrónico?'
            payload_out = payload_message_text(phone, response, False)
            response_out = {'payload_out': payload_out, 'type': 'mail'}
            return response_out
        else:
            # response = menu_message(phone)
            name_db = get_name(phone)
            response = 'Que tal ' + name_db + ', ¿En que te podemos ayudar?'
            payload_out = response
            response_out = {'payload_out': payload_out, 'type': 'menu'}
            return response_out
    except Exception as ex:
        print(ex)
        return "Error"


def menu_message(phone):
    try:
        payload = payload_message_list(phone, "Nos ayudas a seleccionar una opción para apoyarte", "menu", [
            {
                "id": "informes",
                "title": "Informes"
            },
            {
                "id": "cita",
                "title": "Genera una cita"
            },
            {
                "id": "inscribir",
                "title": "Inscripciones"
            },
            {
                "id": "otro",
                "title": "Otro"
            }
        ])
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] menu_payload")
        print("[ERROR] ", ex)
        logging.error("menu_payload")
        logging.error(ex)


def informes(phone):
    try:
        payload = payload_message_list(phone, "En que nivel estas interesado", "niveles", [
            {
                "id": "1p",
                "title": "Primaria"
            },
            {
                "id": "2s",
                "title": "Secundaria"
            },
            {
                "id": "3b",
                "title": "Bachillerato"
            }
        ])
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] menu_payload")
        print("[ERROR] ", ex)
        logging.error("menu_payload")
        logging.error(ex)


def niveles(phone, nivel):
    try:
        if nivel == '_primaria_':
            text_message = "Descubra la oferta académica de nivel primaria en el Colegio Jimbo, donde proporcionamos una educación de calidad con docentes altamente calificados y un plan de estudios integral. \n" \
                           "Nuestro enfoque en valores, tecnología educativa de vanguardia y actividades extracurriculares enriquecen la experiencia educativa de los estudiantes. \n" \
                           "¡Preparamos a los niños para un futuro brillante en un ambiente de aprendizaje seguro y acogedor! "
        elif nivel == '_secundaria_':
            text_message = "Descubra la oferta de nivel secundaria en el Colegio Jimbo, con un enfoque destacado en el idioma inglés. \n" \
                           "Ofrecemos educación de calidad, programas de intercambio, certificaciones internacionales y atención individualizada para preparar a los estudiantes para un mundo globalizado. \n" \
                           "Únase a nosotros para una experiencia educativa enriquecedora y bilingüe que abrirá puertas a un futuro prometedor. \n"
        elif nivel == '_bachillerato_':
            text_message = "Descubra la oferta académica de nivel bachillerato en el Colegio Jimbo, donde ofrecemos una amplia variedad de becas para estudiantes talentosos y dedicados. \n" \
                           "Nuestras becas abarcan áreas académicas, deportivas, artísticas, servicio comunitario, diversidad e inclusión, y liderazgo. \n" \
                           "En Jimbo, estamos comprometidos en brindar una educación de calidad accesible para todos, preparando a los estudiantes para un futuro exitoso y enriquecedor.  \n" \
                           "Contáctenos hoy para obtener más detalles sobre nuestras becas y programas de bachillerato."

        payload = payload_message_text(phone, text_message, False)
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] niveles_payload")
        print("[ERROR] ", ex)
        logging.error("niveles_payload")
        logging.error(ex)


def appoiment_button(phone):
    try:
        payload = payload_message_button(phone, "¿Deseas agendar una cita?",
                                         [{"id": "confirm", "title": "✅ Si me gustaria"},
                                          {"id": "noconfirm", "title": "❌ No, gracias"}])
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] appoiment_button")
        print("[ERROR] ", ex)
        logging.error("appoiment_button")
        logging.error(ex)


def step1_appoinment(phone):
    try:
        fecha_actual = datetime.now()
        day1 = sumar_dias_habiles(fecha_actual, 1)
        day2 = sumar_dias_habiles(fecha_actual, 2)
        day3 = sumar_dias_habiles(fecha_actual, 3)
        day4 = sumar_dias_habiles(fecha_actual, 4)

        payload = payload_message_list(phone, "Qué día te gustaría visitarnos", "Fechas", [
            {
                "id": "date1",
                "title": f"{day1.strftime('%d-%m-%Y')}"
            },
            {
                "id": "date2",
                "title": f"{day2.strftime('%d-%m-%Y')}"
            },
            {
                "id": "date3",
                "title": f"{day3.strftime('%d-%m-%Y')}"
            },
            {
                "id": "date4",
                "title": f"{day4.strftime('%d-%m-%Y')}"
            }
        ])
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] step1_appoinment")
        print("[ERROR] ", ex)
        logging.error("step1_appoinment")
        logging.error(ex)


def get_apoiment_time(phone, date):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = f"""SELECT time_work FROM slots_settings ss  WHERE time_work NOT IN (SELECT time FROM dates d WHERE d.id_agent= ss.id_agent AND d.date=STR_TO_DATE('{date}', '%d-%m-%Y')) AND ss.id_agent='5ec50ee8-57f5-11ee-944c-000d3a5530dx' """
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as ex:
        print("[ERROR] get_apoiment_time")
        print("[ERROR] ", ex)
        logging.error("get_apoiment_time")
        logging.error(ex)


def step2_appoinment(phone, date):
    try:
        time_list = get_apoiment_time(phone, date)
        items = []
        count = 0
        for item in time_list:
            count = count + 1
            delta = item[0]
            horas = delta.seconds // 3600  # 3600 segundos en una hora
            minutos = (delta.seconds % 3600) // 60  # 60 segundos en un minuto
            items.append({"id": f"time_{count}_{date}", "title": f"{horas:02d}:{minutos:02d}"})
        payload = payload_message_list(phone, "¿En que horario?", "Horarios disponibles", items)
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] step2_appoinment")
        print("[ERROR] ", ex)
        logging.error("step2_appoinment")
        logging.error(ex)


def step3_appoinment(phone, date, time):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = f"""INSERT INTO dates (id_agent, date, time,id_person,status) SELECT '5ec50ee8-57f5-11ee-944c-000d3a5530dx', STR_TO_DATE('{date}', '%d-%m-%Y'), '{time}',id,'active' FROM person p WHERE phone='{phone}' """
        cur.execute(sql)
        conn.commit()
        conn.close()
        message_text = f"Tu cita ha sido agendada para el día {date} a las {time} \n" \
                       f"Te esperamos en Jimbo"
        payload = payload_message_text(phone, message_text, False)
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] step3_appoinment")
        print("[ERROR] ", ex)
        logging.error("step3_appoinment")
        logging.error(ex)


def ubicaciones(phone, id):
    try:
        sucursales_1 = [
            {
                "id": "1",
                "title": "Cuautitlán I. El Cerrito"
            }, {
                "id": "2",
                "title": "Cuautitlán I. C.Urbano"
            }, {
                "id": "3",
                "title": "Tlalnepantla Tlalnemex"
            }, {
                "id": "4",
                "title": "Tlalnepantla La Loma"
            }, {
                "id": "5",
                "title": "Tlanepantla Galeana"
            }, {
                "id": "mas ubicaciones",
                "title": "Otras ubicaciones"
            }]
        sucursales_2 = [{
            "id": "6",
            "title": "Aguascalientes"
        }, {
            "id": "7",
            "title": "Puerto Vallarta"
        }, {
            "id": "8",
            "title": "Guadalajara"
        }, {
            "id": "9",
            "title": "Querétaro"
        }, {
            "id": "10",
            "title": "San Juan Del Rio"
        }, {
            "id": "11",
            "title": "Ciudad de México"
        }]
        payload_ubicaciones = []
        body_in = ''
        if id == 1:
            payload_ubicaciones = sucursales_1
            body_in = '¿A qué sucursal quieres contactar?'
        elif id == 2:
            payload_ubicaciones = sucursales_2
            body_in = 'Otras opciones'

        payload = payload_message_list(phone, body_in, "Ubicaciones", payload_ubicaciones)
        response = payload
        return response
    except Exception as ex:
        print("[ERROR] ubicaciones")
        print("[ERROR] ", ex)
        logging.error("ubicaciones")
        logging.error(ex)


def event_graph_api(date, time, name, mail, phone):
    anio = date.split("-")[2]
    mes = date.split("-")[1]
    dia = date.split("-")[0]
    start_datetime = anio + "-" + mes + "-" + dia + "T" + time + ":00"
    formato = '%Y-%m-%dT%H:%M:%S'
    tiempo_objeto = datetime.strptime(start_datetime, formato)
    tiempo_sumado = tiempo_objeto + timedelta(hours=1)
    end_datetime = tiempo_sumado.isoformat()
    # Microsoft Graph API endpoints
    graph_api_endpoint = 'https://graph.microsoft.com'
    version = 'v1.0'
    events_endpoint = f'{graph_api_endpoint}/' + f'{version}/users/omar.rosales@mattilda.io/events'
    print(events_endpoint)
    # Replace these values with your actual credentials and tenant ID
    client_id = '6300a05d-027f-4a63-be59-fcd29c1c71ed'
    client_secret = '.Y18Q~WVA76_lBKwYobkuRZVXAoC3Gczf8pmlbfu'
    tenant_id = '58656efd-4911-4c95-a061-161d6432ad0f'

    # Construct the token endpoint URL
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    # Define the event details
    event_details = {
        "subject": "Reunion agendada por WhatsApp",
        "body": {
            "contentType": "HTML",
            "content": "Sesion agendada mediante un chatbot de WhatsApp"
        },
        "start": {
            "dateTime": f"{start_datetime}",
            "timeZone": "Central Standard Time"
        },
        "end": {
            "dateTime": f"{end_datetime}",
            "timeZone": "Central Standard Time"
        },
        "location": {
            "displayName": "Session de WhatsApp"
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": f"{mail}",
                    "name": f"{name}"
                },
                "type": "required"
            }
        ],
        "responseRequested": True,
        "allowNewTimeProposals": True,
        "isOnlineMeeting": True,  # Indicate it's an online meeting
        "onlineMeetingProvider": "teamsForBusiness"
    }
    print(token_url)
    # Obtain access token using client credentials flow
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': f'{graph_api_endpoint}/.default'
    }

    token_r = requests.post(token_url, data=token_data)
    print(token_r)
    token = token_r.json().get('access_token')
    print('Access token:', token)
    # Create the event using the access token
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    create_event_response = requests.post(events_endpoint, headers=headers, json=event_details)

    if create_event_response.status_code == 201:
        print('Event created successfully.')
        created_event = create_event_response.json()
        print('Event ID:', created_event['id'])
    else:
        print('Failed to create event. Status code:', create_event_response.status_code)
        print('Error message:', create_event_response.text)


def event_outlook(date, time, name, mail, phone):
    try:
        anio = date.split("-")[2]
        mes = date.split("-")[1]
        dia = date.split("-")[0]
        hora = time.split(":")[0]
        minuto = time.split(":")[1]
        tz = pytz.timezone('America/Mexico_City')
        start = datetime(int(anio), int(mes), int(dia), int(hora), int(minuto), tzinfo=tz)
        star_calendar = start - datetime.timedelta(hours=0)
        end_calendar = star_calendar + datetime.timedelta(hours=1)

        # Configura las credenciales
        # username = os.getenv('USERNAME_MAIL')
        # password = os.getenv('PASSWORD_MAIL')
        username = 'gonzomj@hotmail.com'
        password = 'OMARTINEZ07'
        print(username)
        print(password)
        credentials = Credentials(username, password)
        config = Configuration(server='outlook.office365.com', credentials=credentials)
        # Configura la cuenta
        account = Account(username, credentials=credentials, config=config, autodiscover=False, access_type=DELEGATE)
        print(account)
        # Crea un nuevo evento en el calendario
        event = CalendarItem(
            account=account,
            folder=account.calendar,  # Especifica la carpeta de calendario de destino
            subject='Reunion con ' + name,
            body=HTMLBody('Cita agendada desde WhatsApp'),
            location='Presencial',
            start=star_calendar,  # Puedes personalizar la fecha y hora
            end=end_calendar,  # Puedes personalizar la fecha y hora
        )
        event.required_attendees = [mail]
        # event.optional_attendees = ['   ']
        event.reminder_minutes_before_start = 15
        # event.is_all_day = False
        # event.is_cancelled = False
        event.is_meeting = True
        # event.is_recurring = False
        event.is_response_requested = True
        # event.is_resend = False
        # event.is_submitted = False
        # event.is_unmodified = False
        # event.meeting_request_type = 'NewMeetingRequest'
        # event.meeting_request_was_sent = True
        # event.response_type = 'Organizer'
        event.save(send_meeting_invitations='SendToAllAndSaveCopy')
        # Guarda el evento en el calendario
        # event.save()
    except Exception as ex:
        print("[ERROR] event_outlook")
        print("[ERROR] ", ex)
        logging.error("event_outlook")
        logging.error(ex)


def response_bot(phone, name, message, wa_id, timestamp, status_phone, id):
    try:
        body = message
        if id != None:
            message = id
        message = unidecode(message.lower())
        if 'time_' in message:
            message = 'time'
        bot_response = bot_chat(message)
        if bot_response == '_saludo_':
            f_response = saludo(phone)
            type_message = f_response['type']
            insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, type_message,
                           status_phone)
            send_message(f_response['payload_out'])
            # if type_message == 'saludo':
            #     response = '¿Cual es tu nombre?'
            #     payload_text = payload_message_text(phone, response, False)
            #     insert_message(phone, str(name), str(message), str(response), wa_id, timestamp, 'name', status_phone)
            #     send_message(payload_text)
        # elif bot_response == '_nombre_':
        #     f_response = nombre(phone, message)
        #     type_message = f_response['type']
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, type_message,
        #                    status_phone)
        #     send_message(f_response['payload_out'])
        # elif get_last_message(phone)[0][2] == 'name':
        #     name = extract_name(message)
        #     update_name(phone, name)
        #     response = 'Hola ' + name + ', ¿Cual es tu correo electrónico?'
        #     insert_message(phone, str(name), str(message), str(response), wa_id, timestamp, 'mail', status_phone)
        #     send_message(payload_message_text(phone, response, False))
        # elif get_last_message(phone)[0][2] == 'mail':
        #     response = 'Gracias!, ¿A que empresa perteneces?'
        #     insert_message(phone, str(name), str(message), str(response), wa_id, timestamp, 'company', status_phone)
        #     send_message(payload_message_text(phone, response, False))
        # elif get_last_message(phone)[0][2] == 'company':
        #     update_company(phone, message)
        #     response = 'Cuéntanos, ¿En que te podemos ayudar?'
        #     insert_message(phone, str(name), str(message), str(response), wa_id, timestamp, 'text', status_phone)
        #     send_message(payload_message_text(phone, response, False))
        # elif bot_response == '_ubicaciones_':
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'list', status_phone)
        #     send_message(ubicaciones(phone, 1))
        # elif bot_response == '_ubicaciones2_':
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'list', status_phone)
        #     send_message(ubicaciones(phone, 2))
        # elif bot_response == '_cita_':
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'button', status_phone)
        #     send_message(appoiment_button(phone))
        # elif bot_response == '_cita1_':
        #     response = step1_appoinment(phone)
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'cita_1', status_phone)
        #     send_message(response)
        # elif bot_response == '_cita2_':
        #     response = step2_appoinment(phone, body)
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'cita_2', status_phone)
        #     send_message(response)
        # elif bot_response == '_cita3_':
        #     date = id.split("_")[2]
        #     response = step3_appoinment(phone, date, body)
        #     # event_outlook(date, body, get_name(phone), get_email(phone), phone)
        #     event_graph_api(date, body, get_name(phone), get_email(phone), phone)
        #     insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'cita_3', status_phone)
        #     send_message(response)
        elif bot_response == '_AI_':
            response = chat_with_docs(message, db=db)
            # response=''
            insert_message(phone, str(name), str(message), str(response), wa_id, timestamp, 'text', status_phone)
            message_out = payload_message_text(phone, response, False)
            send_message(message_out)
        else:
            insert_message(phone, str(name), str(message), str(bot_response), wa_id, timestamp, 'text', status_phone)
            message_out = payload_message_text(phone, bot_response, False)
            send_message(message_out)
    except Exception as ex:
        print(ex)
        return "Error"


def response_admin(response_id_wa, message):
    phone = get_phone_id_wa(response_id_wa)
    try:
        payload_message_text(phone, str(message), False)
        send_message(payload_message_text(phone, str(message), False))
        return True
    except Exception as ex:
        print("[ERROR] response_admin")
        print("[ERROR] ", ex)
        return False


def get_phone_id_wa(id_wa):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = f"SELECT DISTINCT phone FROM contacts c INNER JOIN messages m ON m.contact_id= c.id WHERE m.id_wa = '{id_wa}'"
        cur.execute(sql)
        phone = cur.fetchone()[0]
        conn.close()
        return phone
    except Exception as ex:
        print("[ERROR] get_phone_id_wa")
        print("[ERROR] ", ex)
        return False


def response_text(sender_id, name, text, wa_id, timestamp):
    try:
        if name == "admin":
            message_admin = "Si deseas contestar a algún invitado, recuerda hacerlo como una respuesta a la conversación para saber el destinatario de tu mensaje"
            payload_message_text(sender_id, message_admin, False)
            send_message(payload_message_text(sender_id, message_admin, False))
            return True
        else:
            response = bot_chat(text)
            if response != "":

                if response != "duda_invitado":
                    insert_message(sender_id, str(name), str(text), str(response), wa_id, timestamp, 'text')
                    payload_message_text(sender_id, str(response), False)
                    send_message(payload_message_text(sender_id, str(response), False))
                else:
                    flag = get_flag_hrs(sender_id[3:])
                    insert_message(sender_id, str(name), str(text), str(response), wa_id, timestamp, 'text')
                    if flag == 1:
                        message_admin = f"*Mensaje de {name}*: {text}"
                        payload_message_text(sender_id, str(message_admin), False)
                        send_message(payload_message_text(sender_id, str(message_admin), False))
                    elif flag == 0:
                        alert_admin(os.getenv("ADMIN_PHONE"), str(name), str(text), sender_id)
            return True

    except Exception as ex:
        print("[ERROR] response_text")
        print("[ERROR] ", ex)
        return False


def get_flag_hrs(phone):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = f"SELECT DISTINCT CASE WHEN TIMESTAMPDIFF(MINUTE, max(m.created_date), now()) < 1400 THEN 1 ELSE 0 END mark_type FROM contacts c INNER JOIN messages m ON m.contact_id = c.id WHERE phone like '%{phone}' and message_out='duda_invitado'"
        cur.execute(sql)
        flag = cur.fetchone()[0]
        conn.close()
        return flag
    except Exception as ex:
        print("[ERROR] get_flag_hrs")
        print("[ERROR] ", ex)
        return False


def alert_admin(phone, name, message, phone_client):
    try:
        token = os.environ.get("TOKEN_WA")
        url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
        payload = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{phone}",
                "type": "template",
                "template": {
                    "name": "alerta_de_mensaje",
                    "language": {"code": "es_MX"},
                    "components": [
                        {
                            "type": "body",
                            "parameters": [{"type": "text", "text": f"{name}"}, {"type": "text", "text": f"{message}"}],
                        },
                    ],
                },
            }
        )
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_text = json.loads(response.text)
        insert_message(phone_client, str(name), str(message), "alerta_enviada", response_text["messages"][0]["id"],
                       datetime.now().timestamp(), 'alert')
        return response.status_code
    except Exception as ex:
        print("[ERROR] alert_admin")
        print("[ERROR] ", ex)
        return False

# if __name__ == "__main__":
#     os.environ['USERNAME_MAIL'] = 'gonzomj@hotmail.com'
#     os.environ['PASSWORD_MAIL'] = 'OMARTINEZ07'
#     event_outlook('17-11-2023', '10:00', 'Omar', 'omar.martinez@mattilda.io', '573015555555')
# credentials = Credentials('gonzomj@hotmail.com', 'OMARTINEZ07')
# account = Account('gonzomj@hotmail.com', credentials=credentials, autodiscover=True)
#
# config = Configuration(server='outlook.office365.com', credentials=credentials)
# account = Account('gonzomj@hotmail.com', credentials=credentials, config = config)
# for item in account.inbox.all().order_by('-datetime_received')[:100]:
#      print(item.subject, item.sender, item.datetime_received)
