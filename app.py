import os
from flask import Flask, request
from dotenv import load_dotenv
from sender import send_message

load_dotenv ()

app = Flask(__name__)

WP_WEBOOK_TOKEN = os.getenv ('WP_WEBOOK_TOKEN')
MSG_WEBOOK_TOKEN = os.getenv ("MSG_WEBOOK_TOKEN")
META_TOKENS = [WP_WEBOOK_TOKEN, MSG_WEBOOK_TOKEN]

@app.get ('/')
def index ():
    """ Home page """
    
    return {
        "status": "success",
        "message": "service running",
        "data": []
    }
    
@app.get ('/webhook/')
def webhook_subscribe ():
    """ Webhook for whatsapp """
    
    # Get url&get variables
    hub_mode = request.args.get ('hub.mode', '')
    hub_challenge = request.args.get ('hub.challenge', '')
    hub_verify_token = request.args.get ('hub.verify_token', '')
    
    if hub_mode == "subscribe": 
    
        # Validate token
        if hub_verify_token not in META_TOKENS:
            return ({
                "status": "error",
                "message": "invalid token",
                "data": []
            }, 401)
        
        return hub_challenge
    
    return ({
        "status": "error",
        "message": "invalid request",
        "data": []
    }, 400)

@app.post ('/wp-webhook/')
def message ():
    
    # Get all post data
    data = request.get_json ()
    
    # Get message data
    try:
        message_data = data["entry"][0]["changes"][0]["value"]["messages"][0]
        message_phone = message_data["from"]
        message_text = message_data["text"]["body"]
    except Exception as e:
        return ({
            "status": "error",
            "message": "invalid request",
            "data": []
        }, 200)
        
    # Fix phone number format
    if message_phone.startswith ("521"):
        message_phone = message_phone.replace ("521", "52")
    
    # Send message
    try:
        send_message(message_phone, message_text)
    except Exception as e:
        pass
    
    return {
        "status": "success",
        "message": "message sent",
        "data": []
    }
    
if __name__ == "__main__":
    app.run (port=5000)