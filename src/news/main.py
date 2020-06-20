from news.sources import Sources
from news.sentiment import SentimentAnalysis
from news.input_parser import FeedRawParser
from news.get_source_data import GetSourceData
import logging

from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"hello": "fastapi"}

@app.get("/news/{source}/{category}")
async def news_source_category(source, category):
    sources = Sources()
    get_data = GetSourceData()
    sentimentanalysis = SentimentAnalysis()
    parser = FeedRawParser()

    final_output = []

    # get source urls
    source_urls_details = sources._get_all_rss_feed_urls_sources(source)

    # get information about the source for a categgiven_sourceory
    for source_url_detail in source_urls_details:
        if source_url_detail.get('category') == category:
            source_url_link = source_url_detail.get('link')
            source_category = source_url_detail.get('category')
            source_name = source_url_detail.get('source')
            source_details = source_url_detail

    # get the actual data
    source_data = get_data.get_source_data(source_url_link)

    # parse the data according to our needs
    parsed_source_data = parser._parse(source_data, source_details, source_category, source_name)

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
        output = [dict for dict in final_output if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
    return final_output



@app.get("/news/{category}")
async def news_source_category(category):
    sources = Sources()
    get_data = GetSourceData()
    sentimentanalysis = SentimentAnalysis()
    parser = FeedRawParser()

    source_urls_details = sources._get_all_rss_feed_urls_category(category)

    source_url_link = []
    source_details = []
    for source_url in source_urls_details:
         if source_url.get('link'):
            source_url_link.append(source_url['link'])
            source_details.append(source_url)   


    # get the actual data
    sources_data = []
    for source_url in source_url_link:
        sources_data.append(get_data.get_source_data(source_url))

    # parse the data according to our needs
    parsed_source_data_all_sources = []
    for source_data, source_detail in zip(sources_data, source_details):
        parsed_source_data_all_sources.append(parser._parse(source_data, source_detail, category))


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
            
            sentiment = sentimentanalysis.sentiment_analysis(text)

            final_dict = {**data, **sentiment}

            per_source_data.append(final_dict)
        final_output.append(per_source_data)
        output = [dict for per_source_data in final_output for dict in per_source_data if dict.get('sentiment') == "positive" or dict.get('sentiment') == "neutral"]
    return output


@app.get("/categories")
async def get_all_categories():
    sources = Sources()
    return sources.get_all_categories()