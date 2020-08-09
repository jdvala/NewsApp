import feedparser
import logging

logger = logging.getLogger(__name__)


class GetSourceData:
    """This class gets the source data from a give source url and parses it using feedparser library.
    """
    def get_source_data(self, source_url):
        """Parse the RSS feed using feedparser and return useable data.

        Args:
            source_url (String): URL link for the rss feed.

        Raises:
            AttributeError: If `source_url` is not a string type.
            ValueError: If no `source_url` is found.

        Returns:
            parsed_output (Dict[List[Dict]]): Parsed output from feedparser. 
        """
        if not isinstance(source_url, str):
            raise AttributeError("Please provide string")
        if not source_url:
            raise ValueError("No source provided. Please provide a source")

        parsed_output = feedparser.parse(source_url)
        if not parsed_output:
            logger.error("No Output from feedparser")
            return
        return parsed_output