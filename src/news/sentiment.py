from bs4 import BeautifulSoup
from textblob import TextBlob
import logging
from flair.models import TextClassifier
from flair.data import Sentence


logger = logging.getLogger(__name__)

class SentimentAnalysis:
    """Run sentiment analysis on text"""
    def __init__(self):
        """Initialize sentiment analysis class with model preference

        Args:
            model (string): Type of model to run sentiment analysis with 
        """
        self.sentiment = None
        self.polarity = None
        self.subjectivity = None
        self.subjectivity_value = None
        self.flair_sentiment_model = TextClassifier.load('en-sentiment')

    def sentiment_analysis(self, text):
        clean_text = self.clean_and_validate_text(text)
        return self.sentiment_analysis_textblob(clean_text)


    def clean_and_validate_text(self, text):
        if not isinstance(text, str):
            logger.error(f"Provided input is not a string but is of class {type(text)}")
            return

        return BeautifulSoup(text, "html.parser").text

    def _predict(self, sentence):
        """Get sentiment of a sentence"""
        s = Sentence(sentence)
        self.flair_sentiment_model.predict(s)
        sentence_sentiment = s.labels
        return sentence_sentiment


    def sentiment_analysis_textblob(self, clean_text):
        #TODO: Clean text function
        # break the sentences
        prediction = self._predict(clean_text)
        
        # [POSITIVE (0.7267)]
        if not prediction:
            logger.error("Cannot evaluate input text for sentiment")
            return
        
        prediction_text, prediction_polarity = str(prediction[0]).split(' ')
        
        
        if prediction_text == "POSITIVE":
            self.sentiment = "positive"
        if prediction_text == "NEGATIVE":
            self.sentiment = "negative"
        if prediction_text == "NEUTRAL":
            self.sentiment = "neutral"


        return{
            "sentiment": self.sentiment,
            "text_used_for_sentiment_analysis": clean_text
        }