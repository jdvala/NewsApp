import feedparser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sources:
    """Define sources"""
    def __init__(self):
        self.sources_dict = {
            "cnbc": "http://www.cnbc.com/id/19746125/device/rss/rss.xml",
            "fortune": "https://fortune.com/feed",
            "finance_times": "https://www.ft.com/?format=rss",
            "investing": "https://www.investing.com/rss/news.rss",
            "seeking_alpha": "https://seekingalpha.com/market_currents.xml",
            "the_economic_times": "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
            "reuters_business": "http://feeds.reuters.com/reuters/businessNews",
            "reuters_company_news": "http://feeds.reuters.com/reuters/companyNews",
            "reuters_bankrutcy_news": "http://feeds.reuters.com/reuters/bankruptcyNews",
            "yahoo_finance": "https://finance.yahoo.com/news/rssindex",
            "financial_post": "https://business.financialpost.com/feed/",
            "bloombergquint": "https://www.bloombergquint.com/feed",
            "arabian_business": "https://www.arabianbusiness.com/?service=rss&x=1",
            "moneyweb": "https://www.moneyweb.co.za/rss",
            "business_daily": "https://www.businessdailyafrica.com/latestrss.rss",
            "business_matter": "https://www.bmmagazine.co.uk/feed/",
            "business_world": "https://www.bworldonline.com/feed/",
            "canadian_business": "https://www.canadianbusiness.com/business-news/feed/",
            "business_news": "https://www.businessnews.com.au/rssfeed/latest.rss",
            "cnn_money": "http://rss.cnn.com/rss/money_topstories.rss",
            "nytimes_business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "nytimes_small_business": "https://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml"
        }

    def source_list(self):
        return [*self.sources_dict]

    def _get_rss_feed_url(self, source):
        if not self.sources_dict.get(source):
            logger.error(f"Source not found {source}")
            return
        return self.sources_dict[source]


    def _get_source(self, source):  # TODO: rename this function
        if not isinstance(source, str):
            raise AttributeError("Please provide string")
        if not source:
            raise AttributeError("No source provided. Please provide a source")
        source_url = self._get_rss_feed_url(source=source)

        parsed_output = feedparser.parse(source_url)
        if not parsed_output:
            logger.error("No Output from feedparser")
            return
        return parsed_output

            


    