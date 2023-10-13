import os
import json
import requests
from dotenv import load_dotenv

load_dotenv ()

WP_TOKEN = os.getenv ('WP_TOKEN')

def send_message (phone:int, message:str="", template:str=""):
    """ Send a message in whatsapp using the meta api

    Args:
        phone (int): to whom the message will be sent
        message (str): custom message to be sent
        template (str): template to be sent
    """
    
    # Validate message or template
    if not message and not template:
        raise Exception ("You must provide a message or a template")

    url = "https://graph.facebook.com/v17.0/147654091761491/messages"

    payload = ""
    if template:
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": f"{phone}",
            "type": "template",
            "template": {
                "name": template,
                "language": {
                "code": "en_US"
                }
            }
        })
        
    if message:
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": f"{phone}",
            "type": "text",
            "text": { 
                "preview_url": True,
                "body": message
            }
        })
        
    headers = {
        'Authorization': f'Bearer {WP_TOKEN}',
        'Content-Type': 'application/json'
    }

    res = requests.request("POST", url, headers=headers, data=payload)
    res.raise_for_status ()
    
    print (f"message send to {phone}")