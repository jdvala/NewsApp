from dateutil.parser import parse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedRawParser:
    """Raw RSS feed parser"""
    def __init__(self):
        # Var for source
        self.source_title = None
        self.source_updated = None
        self.source_image_url = None
        self.source_category = None
        self.source_name = None

        # Vars for entry
        self.entry_title = None
        self.entry_language = None
        self.entry_rss_link = None
        self.entry_article_url = None
        self.entry_summary = None
        self.entry_tags = []
        self.entry_published_on = None

    def _feed_raw_parser(self, raw_input, source_details):
        """Pareser for raw data from feedparser according to out needs.

        # Write here about which attributes we will be using

        Args:
            raw_input (Dict[List[Dict]]): Raw output from feedparser.
            source_details (Dict[str, str]): Details about the source

        Returns:
            [type]: [description]
        """
        parsed_result = self._parse(raw_input)
        if not parsed_result:
            logger.error("Unable to parse input")
        return parsed_result

    def _get_entries(self, raw_input, source_details):
        """Get the entries key from raw ouptut from feedparser

        Args:
            raw_input (Dict[List[Dict]]): Raw output from feedparser
        
        Returns:
            entries (Dict): Entries for a given source
        """
        if not raw_input.get("entries"):
            raise ValueError(f"No entries found for source: {source_details.get('source')}")
        return raw_input["entries"]


    def _get_feed_details(self, raw_input, source_details):
        """Get the feed key from raw ouptut from feedparser

        Args:
            raw_input (Dict[List[Dict]]): Raw output from feedparser
        
        Returns:
            desired_output (List[Dict]): Final Output before sentiment analysis
        """
        if not raw_input.get("feed"):
            raise ValueError(f"No entries found for source: {source_details.get('source')}")
        return raw_input["feed"]



    def _parse(self, raw_input, source_details):
        feed_details = self._get_feed_details(raw_input, source_details)
        entries = self._get_entries(raw_input, source_details)

        desired_output = []
        # Parse feed details
        if feed_details.get("title"):
            self.source_title = feed_details["title"]
        else:
            self.source_title = source_details.get("source")
        if feed_details.get("updated"):
            self.source_updated = feed_details["updated"]
        if feed_details.get("image").get("href"):
            self.source_image_url = feed_details["image"]["href"]
        
        # source details
        if source_details.get("category"):
            self.source_category = source_details["category"]
        if source_details.get("source_name"):
            self.source_name = source_details["source"]

        for entry in entries:
            # Parse entry
            if entry.get("title"):
                self.entry_title = entry["title"]
            if entry.get("title_detail").get("language"):
                self.entry_language = entry["title_detail"]["language"]
            if entry.get("summary"):
                self.entry_summary = entry["summary"]
            if entry.get("link"):
                self.entry_rss_link = entry["link"]
            if entry.get("id"):
                self.entry_article_url = entry["id"]
            if entry.get("tags"):
                for tag_info in entry["tags"]:
                    if tag_info.get("term"):
                        self.entry_tags.append(tag_info["term"])
            if entry.get("published"):
                self.entry_published_on = parse(entry["published"])
            
            desired_output.append({
                "source_title": self.source_title,
                "source_category": self.source_category,
                "source_name": self.source_name,
                "source_updated": self.source_updated,
                "source_image_url": self.source_image_url,
                "entry_title": self.entry_title,
                "entry_language": self.entry_language,
                "entry_summary": self.entry_summary,
                "entry_rss_link": self.entry_rss_link,
                "entry_article_url": self.entry_article_url,
                "entry_tags": self.entry_tags,
                "entry_published_on": self.entry_published_on
            })
        
        return desired_output
