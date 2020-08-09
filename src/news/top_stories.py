import pandas as pd
from news.sources import Sources
from news.sentiment import SentimentAnalysis
from news.input_parser import FeedRawParser
from news.get_source_data import GetSourceData
import logging
from pathlib import Path
from datetime import datetime
import uuid


class TopStories:
    def __init__(self):
        self.df_top_stories = Path(__file__).parent.parent.parent/ "src" /"news" / "assets" / "topstories.csv"
    
    def _get_all_rss_feed_urls_category(self):
        """Get the rss feed urls for a source

        Returns:
            source_and_category (List[Dict[str, str]]): A dictonary of source rss links and its categories.
        """
        source_dataframe = pd.read_csv(self.df_top_stories)
        source_link_details = []
        for index, row in source_dataframe.iterrows():
            source_link_details.append(
                {   
                    "link": row['link'],
                    "category": row['category'],
                    "source": row['source'],
                }
            )

        if not source_link_details:
            raise ValueError("No source_category found")
        
        return source_link_details

    
    def get_all_news_data(self):
        sources = Sources()
        get_data = GetSourceData()
        sentimentanalysis = SentimentAnalysis()
        parser = FeedRawParser()

        source_urls_details = self._get_all_rss_feed_urls_category()

        source_url_link = []
        source_details = []
        source_category = []
        source_name = []
        for source_url in source_urls_details:
            if source_url.get('link'):
                source_url_link.append(source_url['link'])
                source_name.append(source_url['source'])
                source_category.append(source_url['category'])
                source_details.append(source_url)   


        # get the actual data
        sources_data = []
        for source_url in source_url_link:
            sources_data.append(get_data.get_source_data(source_url))

        # parse the data according to our needs
        parsed_source_data_all_sources = []
        for source_data, source_detail, name_of_source, category in zip(sources_data, source_details, source_name, source_category):
            parsed_source_data_all_sources.append(parser._parse(source_data, source_detail, category, name_of_source))


        final_output = []
        for parsed_source_data in parsed_source_data_all_sources:
            per_source_data = []
            for data in parsed_source_data:
              
                sentiment = sentimentanalysis.sentiment_analysis(text=data.get('entry_title'))

                final_dict = {**data, **sentiment}

                per_source_data.append(final_dict)
            final_output.append(per_source_data)
            output = [dict for per_source_data in final_output for dict in per_source_data if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
        return output


    def data_to_push_firebase(self):
        all_news_items = self.get_all_news_data()
        data_to_push = {}
        for index, output in enumerate(all_news_items):
            if not output.get('entry_summary') or not output.get('entry_title'):
                continue
            if output.get('entry_summary') == output.get('entry_title'):
                continue
            original_data = {
                "id": index,
                "article_link": output.get('entry_article_url'),
                "category": output.get('source_category'),
                "source": output.get('source_name'),
                "img_url": output.get('source_image_url'),
                "summary": (output.get('entry_summary')).lstrip(" "),
                "title": output.get('entry_title'),
                "news_date": str(datetime.date(datetime.now())),
                "sentiment_type": output.get('sentiment'),
                "time_stamp": str(output.get('entry_published_on'))
            }
            data_to_push[str(uuid.uuid4())] = original_data
        return data_to_push


        
