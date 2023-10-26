import os
import json
import requests
from dotenv import load_dotenv

load_dotenv ()

HOST = os.getenv ("PRICE_CHECKER_HOST")
API_KEY = os.getenv ("PRICE_CHECKER_API_KEY")

class PriceChaker ():
    
    def __init__ (self, keyword:str):
         
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.keyword = keyword
        self.request_id = 0
        
    def post_keyword (self) -> bool:
        """ Send new keyword to scraper 
        
        Returns:
            bool: True if keyword was sent, False if not
        """
        
        # Send data to api
        url = f"{HOST}/keyword/"

        payload = json.dumps({
            "keyword": self.keyword,
            "api-key": API_KEY
        })

        res = requests.request("POST", url, headers=self.headers, data=payload)
        
        # validate response
        if res.status_code == 200:
            
            # Get request id
            self.request_id = res.json () ["data"]["request-id"]
            return True
        else:
            return False

    def get_status (self) -> str:
        """ Query scraping status 
        
        Returns:
            str: scraping status ("" if error)
        """
        
        # Query data from api
        url = f"{HOST}/status/"

        payload = json.dumps({
            "request-id": self.request_id,
            "api-key": API_KEY
        })

        res = requests.request("POST", url, headers=self.headers, data=payload)

        # validate response
        if res.status_code == 200:
            
            # Validate scraping status 
            scraping_status = res.json () ["data"]["status"]
            return scraping_status
        else:
            return ""

    def get_preview (self) -> str:
        """ Get preview url

        Returns:
            str: preview url
        """

        url = f"{HOST}/preview/?request-id={self.request_id}"
        return url