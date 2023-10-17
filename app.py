import os
from threading import Thread
from flask import Flask, request
from dotenv import load_dotenv
from sender import send_message_msg, send_message_wp
from workflow import workflow

load_dotenv ()

app = Flask(__name__)

WP_WEBOOK_TOKEN = os.getenv ('WP_WEBOOK_TOKEN')
MSG_WEBOOK_TOKEN = os.getenv ("MSG_WEBOOK_TOKEN")
META_TOKENS = [WP_WEBOOK_TOKEN, MSG_WEBOOK_TOKEN]
PORT = int(os.environ.get('PORT', 5000))

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

@app.post ('/webhook/')
def message ():
    
    # Get all post data
    data = request.get_json ()
    
    # Detect if is msg or wp message
    source = "wp"
    entry = data["entry"][0]
    if entry.get ("messaging", ""):
        source = "msg"
        
    
    # Default error
    error_response = ({
        "status": "error",
        "message": "invalid request",
        "data": []
    }, 200)
    
    if source == "wp":
        
        # Get message data
        try:
            message_data = entry["changes"][0]["value"]["messages"][0]
            message_phone = message_data["from"]
            message_text = message_data["text"]["body"]
        except Exception as e:
            return error_response
            
        # Fix phone number format
        if message_phone.startswith ("521"):
            message_phone = message_phone.replace ("521", "52")
        
        # Send message
        workflow_thread = Thread (target=workflow, args=(message_phone, message_text, send_message_wp))
        workflow_thread.start ()
        
    elif source == "msg":
        
        # Get message data
        try:
            message_data = entry["messaging"][0]
            message_sender = message_data["sender"]["id"]
            message_text = message_data["message"]["text"]
        except Exception as e:
            return error_response
            
        # Send message
        workflow_thread = Thread (target=workflow, args=(message_sender, message_text, send_message_msg))
        workflow_thread.start ()        
    
    # Confirm message
    return ("EVENT_RECEIVED", 200)
    
if __name__ == "__main__":
    app.run (port=PORT)