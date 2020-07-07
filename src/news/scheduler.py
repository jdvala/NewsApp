from news.sources import Sources
from news.sentiment import SentimentAnalysis
from news.input_parser import FeedRawParser
from news.get_source_data import GetSourceData
import logging
import uuid

class Scheduler:
    def data_to_push_firebase(self, all_news_items):
        if not all_news_items:
            raise ValueError("No data found")
            return None
        data_to_push = {}
        for index, output in enumerate(all_news_items):
            original_data = {
                "id": index,
                "article_link": output.get('entry_article_url'),
                "category": output.get('source_category'),
                "source": output.get('source_name'),
                "img_url": output.get('source_image_url'),
                "summary": output.get('entry_summary'),
                "title": output.get('entry_title'),
            }
            data_to_push[str(uuid.uuid4())] = original_data            
        return data_to_push
    

    def scheduled_push(self, kvell_db, data):
        kvell_db.child('news_feed').set(data)

    def scheduled_delete(self, kvell_db):
        kvell_db.child('news_feed').remove()


    def get_all_news_data(self):
        sources = Sources()
        get_data = GetSourceData()
        sentimentanalysis = SentimentAnalysis()
        parser = FeedRawParser()


        source_urls_details = sources._get_all_rss_feed_urls_category(is_all=True)

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
                if data.get('entry_title') and data.get('entry_summary'):
                    text = f"{data['entry_title']}. {data['entry_summary']}"
                elif data.get('entry_title') and not data.get('entry_summary'):
                    text = data['entry_title']
                elif not data.get('entry_title') and data.get('entry_summary'):
                    text = data['entry_summary']
                else:
                    raise ValueError("No title or summary found parsed data.")
                
                sentiment = sentimentanalysis.sentiment_analysis(text=text)

                final_dict = {**data, **sentiment}

                per_source_data.append(final_dict)
            final_output.append(per_source_data)
            output = [dict for per_source_data in final_output for dict in per_source_data if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
        return output
