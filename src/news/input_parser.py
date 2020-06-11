from dateutil.parser import parse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedRawParser:
    """Raw RSS feed parser"""
    def __init__(self):
        self.title = ""
        self.language = ""
        self.rss_link = ""
        self.article_url = ""
        self.summary = ""
        self.tags = []
        self.published_on = ""

    def _feed_raw_parser(self, raw_input):
        parsed_result = self._parse_raw_output(raw_input)
        if not parsed_result:
            logger.error("Unable to parse input")
        return parsed_result

    def _parse_raw_output(self, raw_input):
        if raw_input.get("title"):
            self.title = raw_input["title"]
        if raw_input.get("title_detail").get("language"):
            self.language = raw_input["title_detail"]["language"]
        if raw_input.get("summary"):
            self.summary = raw_input["summary"]
        if raw_input.get("link"):
            self.rss_link = raw_input["link"]
        if raw_input.get("id"):
            self.article_url = raw_input["id"]
        if raw_input.get("tags"):
            for tag_info in raw_input["tags"]:
                if tag_info.get("term"):
                    self.tags.append(tag_info["term"])
        if raw_input.get("published"):
            self.published_on = parse(raw_input["published"])
        
        return {
            "title": self.title,
            "language": self.language,
            "summary": self.summary,
            "rss_link": self.rss_link,
            "article_url": self.article_url,
            "tags": self.tags,
            "published_on": self.published_on
        }
