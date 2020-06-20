from news.sources import Sources
from news.sentiment import SentimentAnalysis
from news.input_parser import FeedRawParser
from news.get_source_data import GetSourceData
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Main:
    def combine(self, source):
        sources = Sources()
        get_data = GetSourceData()
        sentimentanalysis = SentimentAnalysis()
        parser = FeedRawParser()
        
        final_output = []
        
        # get source urls
        source_urls = sources._get_all_rss_feed_urls(source)
        
        # get information about first url
        source_url_link = source_urls[0].get('link')
        source_category = source_urls[0].get('category')
        source_source = source_urls[0].get('source')

        # get the actual data
        source_data = get_data.get_source_data(source_url_link)

        # parse the data according to our needs
        parsed_source_data = parser._parse(source_data, source_urls[0])

        final_output = []
        for data in parsed_source_data:
            if data.get('entry_title') and data.get('entry_summary'):
                text = f"{data['entry_title']}. {data['entry_summary']}"
            elif data.get('entry_title') and not data.get('entry_summary'):
                text = data['entry_title']
            elif not data.get('entry_title') and data.get('entry_summary'):
                text = data['entry_summary']
            else:
                raise ValueError("No title or summary found parsed data.")
            
            sentiment = sentimentanalysis.sentiment_analysis(text)

            final_dict = {**data, **sentiment}
        
            final_output.append(final_dict)
        return final_output
        

