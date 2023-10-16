

def workflow (send_to:str, message:str, send_function:callable):
    
    basic_message = 'Hi! Introduce the keyword like this exact format example: "Keyword=plant based protein"'
    wait_message = "We are obtaining the real-time prices for you right now. The process might take around 2 minutes! Hold on!"
    
    # Send basic or wait message
    if "=" in message:
        send_function (send_to, wait_message)
        
        # get keyword
        replace_chars = ["'", '"', ",", ".", "/", "-", "_", "?", "="]
        keyword = message.split ("=")[1]
        for char in replace_chars:
            keyword = keyword.replace (char, " ")
        
    else:
        send_function (send_to, basic_message)