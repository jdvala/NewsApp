from bs4 import BeautifulSoup
from textblob import TextBlob
import logging
# from flair.models import TextClassifier
# from flair.data import Sentence


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalysis:
    """Run sentiment analysis on text"""
    def __init__(self):
        """Initialize sentiment analysis class with model preference

        Args:
            model (string): Type of model to run sentiment analysis with 
        """
        # self.model = model
        self.sentiment = None
        self.polarity = None
        self.subjectivity = None
        self.subjectivity_value = None
        
        # if model = Flair then init flair model
        # if self.model == "Flair":
        #     self.classifier = TextClassifier.load('en-sentiment')

    def sentiment_analysis(self, text):
        clean_text = self._clean_and_validate_text(text)
        # if self.model == "Flair":
        #     return self.sentiment_analysis_flair(clean_text)
        return self.sentiment_analysis_textblob(clean_text)


    def _clean_and_validate_text(self, text):
        if not isinstance(text, str):
            logger.error(f"Provided input is not a string but is of class {type(text)}")
            return

        return BeautifulSoup(text, "html.parser").text

    # def sentiment_analysis_flair(self, clean_text):
    #     text_flair = Sentence(clean_text)
    #     classification = self.classifier(text_flair)
    #     if not classification.lable:
    #         logger.error(f"Flair could not classify the text {text_flair}.")
    #         raise ValueError("Flair classification failed.")
    #     # TODO: Add polarity value [Positive (1.0)] from label
    #     return{
    #         "sentiment": classification.lable,
    #     }

    def sentiment_analysis_textblob(self, clean_text):
        text_blob = TextBlob(clean_text)

        if not text_blob.sentiment:
            logger.error("Cannot evaluate input text for sentiment")
            return
        
        if text_blob.sentiment.polarity > 0:
            self.sentiment = "positive"
        if text_blob.sentiment.polarity < 0:
            self.sentiment = "negative"
        if text_blob.sentiment.polarity == 0:
            self.sentiment = "neutral"
        
        if text_blob.sentiment.subjectivity > 0:
            self.subjectivity = "subjective"
        if text_blob.sentiment.subjectivity < 0:
            self.subjectivity = "objective"

        return{
            "sentiment": self.sentiment,
            "polarity": text_blob.sentiment.polarity,
            "subjectivity/objectivity": self.subjectivity,
            "subjectivity/objectivity_value": text_blob.sentiment.subjectivity,
            "text_used_for_sentiment_analysis": clean_text
        }