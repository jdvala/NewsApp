from scheduler import Scheduler
import schedule
from database import FirebaseDB
import time
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# initilize database once
firebase = FirebaseDB()
logger.info("Database init complete")

def main():
    scheduler = Scheduler()

    # collect all the data
    news_data = scheduler.get_all_news_data()
    logger.info("All news data collected")
    data_for_push = scheduler.data_to_push_firebase(news_data)
    logger.info("Data ready to be pushed")
    start_time = time.time()
    # remove the old data populated int the database
    scheduler.scheduled_delete(firebase.kvell_database())
    logger.info("Data deleted")
    
    # populate the database
    scheduler.scheduled_push(firebase.kvell_database(), data_for_push)
    logger.info("Data pushed")
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == "__main__":
    main()
    # schedule.every().hour.do(main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    
# from news.sources import Sources
# from news.sentiment import SentimentAnalysis
# from news.input_parser import FeedRawParser
# from news.get_source_data import GetSourceData
# import logging

# from fastapi import FastAPI

# app = FastAPI()

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# @app.get("/")
# async def root():
#     return {"hello": "fastapi"}

# @app.get("/news/{source}/{category}")
# async def news_source_category(source, category):
#     """Get news for a specific source and sepcific categry.

#     Args:
#         source (string): Souce name.
#         category (string): Category of news

#     Raises:
#         ValueError: If `Summary` or `Text` is not found in the the parsed news rss feed. 

#     Returns:
#         final_output [List[Dict]]: News from a specified source and category.
#     """
#     sources = Sources()
#     get_data = GetSourceData()
#     sentimentanalysis = SentimentAnalysis()
#     parser = FeedRawParser()

#     final_output = []

#     # get source urls
#     source_urls_details = sources._get_all_rss_feed_urls_sources(source)

#     # get information about the source for a categgiven_sourceory
#     for source_url_detail in source_urls_details:
#         if source_url_detail.get('category') == category:
#             source_url_link = source_url_detail.get('link')
#             source_category = source_url_detail.get('category')
#             source_name = source_url_detail.get('source')
#             source_details = source_url_detail

#     # get the actual data
#     source_data = get_data.get_source_data(source_url_link)

#     # parse the data according to our needs
#     parsed_source_data = parser._parse(source_data, source_details, source_category, source_name)

#     final_output = []
#     for data in parsed_source_data:
#         if data.get('entry_title') and data.get('entry_summary'):
#             text = f"{data['entry_title']}. {data['entry_summary']}"
#         elif data.get('entry_title') and not data.get('entry_summary'):
#             text = data['entry_title']
#         elif not data.get('entry_title') and data.get('entry_summary'):
#             text = data['entry_summary']
#         else:
#             raise ValueError("No title or summary found parsed data.")
        
#         sentiment = sentimentanalysis.sentiment_analysis(text=text)

#         final_dict = {**data, **sentiment}

#         final_output.append(final_dict)
#         output = [dict for dict in final_output if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
#     return final_output


# @app.get("/all")
# async def get_all_news():
#     sources = Sources()
#     get_data = GetSourceData()
#     sentimentanalysis = SentimentAnalysis()
#     parser = FeedRawParser()


#     source_urls_details = sources._get_all_rss_feed_urls_category(is_all=True)

#     source_url_link = []
#     source_details = []
#     source_category = []
#     source_name = []
#     for source_url in source_urls_details:
#          if source_url.get('link'):
#             source_url_link.append(source_url['link'])
#             source_name.append(source_url['source'])
#             source_category.append(source_url['category'])
#             source_details.append(source_url)   


#     # get the actual data
#     sources_data = []
#     for source_url in source_url_link:
#         sources_data.append(get_data.get_source_data(source_url))

#     # parse the data according to our needs
#     parsed_source_data_all_sources = []
#     for source_data, source_detail, name_of_source, category in zip(sources_data, source_details, source_name, source_category):
#         parsed_source_data_all_sources.append(parser._parse(source_data, source_detail, category, name_of_source))


#     final_output = []
#     for parsed_source_data in parsed_source_data_all_sources:
#         per_source_data = []
#         for data in parsed_source_data:
#             if data.get('entry_title') and data.get('entry_summary'):
#                 text = f"{data['entry_title']}. {data['entry_summary']}"
#             elif data.get('entry_title') and not data.get('entry_summary'):
#                 text = data['entry_title']
#             elif not data.get('entry_title') and data.get('entry_summary'):
#                 text = data['entry_summary']
#             else:
#                 raise ValueError("No title or summary found parsed data.")
            
#             sentiment = sentimentanalysis.sentiment_analysis(text=text)

#             final_dict = {**data, **sentiment}

#             per_source_data.append(final_dict)
#         final_output.append(per_source_data)
#         output = [dict for per_source_data in final_output for dict in per_source_data if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
#     return output



# @app.get("/news/{category}")
# async def news_source_category(category):
#     """Get news per category.

#     Args:
#         category (string): News category you want to query

#     Raises:
#         ValueError: If `Summary` or `Text` is not found in the the parsed news rss feed.

#     Returns:
#         output [List[List[Dict]]]: News of category sepcified from all the sources.
#     """
#     sources = Sources()
#     get_data = GetSourceData()
#     sentimentanalysis = SentimentAnalysis()
#     parser = FeedRawParser()

#     source_urls_details = sources._get_all_rss_feed_urls_category(category)

#     source_url_link = []
#     source_details = []
#     source_name = []
#     for source_url in source_urls_details:
#          if source_url.get('link'):
#             source_url_link.append(source_url['link'])
#             source_name.append(source_url['source'])
#             source_details.append(source_url)   


#     # get the actual data
#     sources_data = []
#     for source_url in source_url_link:
#         sources_data.append(get_data.get_source_data(source_url))

#     # parse the data according to our needs
#     parsed_source_data_all_sources = []
#     for source_data, source_detail, name_of_source in zip(sources_data, source_details, source_name):
#         parsed_source_data_all_sources.append(parser._parse(source_data, source_detail, category, name_of_source))


#     final_output = []
#     for parsed_source_data in parsed_source_data_all_sources:
#         per_source_data = []
#         for data in parsed_source_data:
#             if data.get('entry_title') and data.get('entry_summary'):
#                 text = f"{data['entry_title']}. {data['entry_summary']}"
#             elif data.get('entry_title') and not data.get('entry_summary'):
#                 text = data['entry_title']
#             elif not data.get('entry_title') and data.get('entry_summary'):
#                 text = data['entry_summary']
#             else:
#                 raise ValueError("No title or summary found parsed data.")
            
#             sentiment = sentimentanalysis.sentiment_analysis(text=text)

#             final_dict = {**data, **sentiment}

#             per_source_data.append(final_dict)
#         final_output.append(per_source_data)
#         output = [dict for per_source_data in final_output for dict in per_source_data if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
#     return output


# @app.get("/categories")
# async def get_all_categories():
#     sources = Sources()
#     return sources.get_all_categories()