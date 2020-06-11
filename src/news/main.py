from news.sources import Sources
from news.sentiment import SentimentAnalysis
from news.input_parser import FeedRawParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Main:
    def combine(self, source):
        sources = Sources()
        sentimentanalysis = SentimentAnalysis()
        parser = FeedRawParser()
        final_output = []
        feed_parsed = sources._get_source(source=source)
        
        if not feed_parsed.get('entries'):
            logger.error(f"No entries found for source {source}")

        for entry in feed_parsed['entries']:
            # parse it
            parsed_output = parser._feed_raw_parser(entry)

            if parsed_output.get("summary") and parsed_output.get("title"):
                sentiments = sentimentanalysis.sentiment_analysis(f"{parsed_output['title']}\n{parsed_output['summary']}")
            elif parsed_output.get("title"):
                logger.info("No summary found running sentiment analysis on title")
                if parsed_output.get("title"):
                    sentiments = sentimentanalysis.sentiment_analysis(parsed_output["title"])
            
            if sentiments:
                final_output.append({**parsed_output, **sentiments})
            else:
                final_output.append(parsed_output)

        return final_output
            
