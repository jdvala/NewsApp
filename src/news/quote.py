import logging
import requests

logger = logging.getLogger(__name__)

class GetQuote:
    def __init__(self):
        self.quote_url = "http://quotes.rest/qod.json?category=inspire"
        self.placeholder = {
                                "quote": "A man is but a product of his thoughts. What he thinks he becomes",
                                "author": "Mahatma Gandhi"
                        }
        
    def get_quote(self):
        """Request quotes API"""
        try:
            response = requests.get(self.quote_url)
        except requests.exceptions.RequestException as exc:
            logger.error("Quotes API resquest error", exc_info=exc)
            return self.placeholder
        
        if not response.ok:
            logger.error("No response from Quotes API ")
            return self.placeholder
        quote_data = response.json()

        if not quote_data.get("contents"):
            return self.placeholder
        logging.info("Quotes sent succesfully")
        return {
            "quote": quote_data['contents']['quotes'][0]['quote'],
            "author": quote_data['contents']['quotes'][0]['author']
        }
            