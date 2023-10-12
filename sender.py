import os
import json
import requests
from dotenv import load_dotenv

load_dotenv ()

WP_TOKEN = os.getenv ('WP_TOKEN')

def send_message (phone:int, message:str):
    """ Send a message in whatsapp using the meta api

    Args:
        phone (int): to whom the message will be sent
        message (str): message to be sent
    """
    

    url = "https://graph.facebook.com/v17.0/147654091761491/messages"

    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": f"{phone}",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
            "code": "en_US"
            }
        }
    })
    headers = {
        'Authorization': f'Bearer {WP_TOKEN}',
        'Content-Type': 'application/json'
    }

    res = requests.request("POST", url, headers=headers, data=payload)
    res.raise_for_status ()
    
    print (f"message send to {phone}")

send_message (527295162472, "hello world")