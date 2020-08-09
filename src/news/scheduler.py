from news.sources import Sources
from news.sentiment import SentimentAnalysis
from news.input_parser import FeedRawParser
from news.get_source_data import GetSourceData
import logging
from tqdm import tqdm
from datetime import datetime
import uuid

class Scheduler:
    def data_to_push_firebase(self, all_news_items):
        if not all_news_items:
            raise ValueError("No data found")
            return None
        data_to_push = {}
        all_categories = []
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
            all_categories.append(output.get('source_category'))
            data_to_push[str(uuid.uuid4())] = original_data

        unique_categories = list(set(all_categories))
        sorted_categories = sorted(unique_categories)
        sorted_categories.insert(0, "All")
        categories = dict(zip(range(len(unique_categories)), sorted_categories))
        return data_to_push, categories
    

    def scheduled_push(self, kvell_db, data, categories, motivational_news, top_stories):
        kvell_db.child('categories').set(categories)
        kvell_db.child('news_feed').set(data)
        kvell_db.child('motivational').set(motivational_news)
        kvell_db.child('top_stories').set(top_stories)

    def scheduled_delete(self, kvell_db):
        a = [kvell_db.child('categories').child(a).remove() for a in  kvell_db.child('categories').get().key()]
        b = [kvell_db.child('news_feed').child(a).remove() for a in  kvell_db.child('news_feed').get().key()]
        c = [kvell_db.child('motivational').child(a).remove() for a in  kvell_db.child('motivational').get().key()]
        d = [kvell_db.child('top_stories').child(a).remove() for a in  kvell_db.child('top_stories').get().key()]
        # kvell_db.child('news_feed').remove()
        # kvell_db.child('motivational').remove()
        # kvell_db.child('top_stories').remove()


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
        for source_url in tqdm(source_url_link, desc="Loading Source Data"):
            sources_data.append(get_data.get_source_data(source_url))

        # parse the data according to our needs
        parsed_source_data_all_sources = []
        for source_data, source_detail, name_of_source, category in zip(tqdm(sources_data, desc="Parsing Data"), source_details, source_name, source_category):
            parsed_source_data_all_sources.append(parser._parse(source_data, source_detail, category, name_of_source))


        final_output = []
        for parsed_source_data in tqdm(parsed_source_data_all_sources,desc="Performing Sentiment Analysis"):
            per_source_data = []
            for data in parsed_source_data:
              
                sentiment = sentimentanalysis.sentiment_analysis(text=data.get('entry_title'))

                final_dict = {**data, **sentiment}

                per_source_data.append(final_dict)
            final_output.append(per_source_data)
            output = [dict for per_source_data in final_output for dict in per_source_data if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
        return output
