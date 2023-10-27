from time import sleep
from api import Api

def workflow (send_to:str, message:str, send_function:callable):
    
    basic_message = 'Hi! Introduce the keyword like this exact format example: "Keyword=plant based protein"'
    wait_message = "We are obtaining the real-time prices for you right now. The process might take around 2 minutes! Hold on!"
    error_message = "Meta is not working correctly right now. Please try again later!"
    preview_message = "Grab here your comparative (ultra-safe link 🔒): \n\n"
    
    # Send basic or wait message
    if "=" in message:
        send_function (send_to, wait_message)
        
        # get keyword
        replace_chars = ["'", '"', ",", ".", "/", "-", "_", "?", "="]
        keyword = message.split ("=")[1]
        for char in replace_chars:
            keyword = keyword.replace (char, " ")
            
        # Connect to price checker
        api = Api (keyword)
        keyword_sent = api.post_keyword ()
        if not keyword_sent:
            send_function (send_to, error_message)
            return None
        
        # Wait for scraping status "done"
        while True:
            
            sleep (15)
            
            # Get scraping status
            scraping_status = api.get_status ()
            
            # Detect errors
            if not scraping_status:
                send_function (send_to, error_message)
                return None
            
            # End loop
            if scraping_status == "done":
                break
        
        # Get preview url
        preview_url = api.get_preview ()
        preview_message += preview_url
        send_function (send_to, preview_message)
        
    else:
        send_function (send_to, basic_message)