
from fastapi import FastAPI, Request
import requests
import json

app = FastAPI()

FB_GRAPH_BASE_URL = 'https://graph.facebook.com/v15.0'
PAGE_ID = '<page_id>'
PAGE_ACCESS_TOKEN = '<page_access_token>'

@app.post("/send-message")
async def send_message(request: Request):
    post_data = await request.json()
    message = post_data['message']

    conversations_params = {
        'fields': 'participants',
        'access_token': PAGE_ACCESS_TOKEN,
    }

    if post_data.get('platform') == 'instagram':
        conversations_params['platform'] = 'instagram'

    conversations = requests.get(
        f'{FB_GRAPH_BASE_URL}/{PAGE_ID}/conversations',
        params=conversations_params)

    customer_psid = conversations.json()['data'][0]['participants']['data'][1]['id']

    message_params = {
        'recipient': json.dumps({'id': customer_psid}),
        'message': json.dumps({'text': message}),
        'messaging_type': 'RESPONSE',
        'access_token': PAGE_ACCESS_TOKEN,
    }

    if post_data.get('platform') == 'instagram':
        message_params['platform'] = 'instagram'

    response = requests.post(
        f"{FB_GRAPH_BASE_URL}/{PAGE_ID}/messages",
        params=message_params)

    return {"status": "success", "response": response.json()}

# rutas y lógica del servidor 