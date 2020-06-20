from bs4 import BeautifulSoup
from textblob import TextBlob
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalysis:
    """Run sentiment analysis on text"""
    def __init__(self):
        self.sentiment = ""
        self.polarity = ""
        self.subjectivity = ""
        self.subjectivity_value = ""

    def _clean_text(self, text):
        return BeautifulSoup(text, "html.parser").text

    def sentiment_analysis(self, text):
        if not isinstance(text, str):
            logger.error(f"Provided input is not a string but is of class {type(text)}")
            return
        clean_text = self._clean_text(text)
        if not clean_text:
            logger.error(f"Can not clean input text {text}")
            return
        blob = TextBlob(text)

        if not blob.sentiment:
            logger.error("Cannot evaluate input text for sentiment")
            return
        
        if blob.sentiment.polarity > 0:
            self.sentiment = "positive"
        if blob.sentiment.polarity < 0:
            self.sentiment = "negative"
        if blob.sentiment.polarity == 0:
            self.sentiment = "neutral"
        
        if blob.sentiment.subjectivity > 0:
            self.subjectivity = "subjective"
        if blob.sentiment.subjectivity < 0:
            self.subjectivity = "objective"

        return{
            "sentiment": self.sentiment,
            "polarity": blob.sentiment.polarity,
            "subjectivity/objectivity": self.subjectivity,
            "subjectivity/objectivity_value": blob.sentiment.subjectivity,
            "text_used_for_sentiment_analysis": clean_text
        }