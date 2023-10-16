import os
import json
import requests
from dotenv import load_dotenv

load_dotenv ()

WP_TOKEN = os.getenv ('WP_TOKEN')
MSG_TOKEN = os.getenv ("MSG_TOKEN")
MSG_PAGE_ID = os.getenv ("MSG_PAGE_ID")

def send_message_wp (phone:int, message:str="", template:str=""):
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
    
def send_message_msg (recipient_id:int, message:str=""):
    """ Send a message in whatsapp using the meta api

    Args:
        recipient_id (int): to whom the message will be sent
        message (str): custom message to be sent
    """

    url = f"https://graph.facebook.com/v18.0/{MSG_PAGE_ID}/messages/?access_token={MSG_TOKEN}"

    payload = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": message
        }
    })
        
    headers = {
        'Content-Type': 'application/json'
    }

    res = requests.request("POST", url, headers=headers, data=payload)
    res.raise_for_status ()
    
    print (f"message send to {recipient_id}")