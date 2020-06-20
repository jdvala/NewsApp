import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sources:
    """Define sources"""
    def __init__(self):
       self.df_path = Path(".").parent.parent / "assets" / "sources.csv"
    
    def _load_dataframe(self):
        df = pd.read_csv(self.df_path)
        if df.empty:
            logger.error("Source dataframe empty")
        return df

    
    def source_list(self):
        """This function generates sources list from the sources dataframe

        Returns:
            sources (List): The list of all the sources we currently offer
        """
        dataframe = self._load_dataframe()
        sources_from_dataframe = dataframe['sources'].tolist()
        return sources_from_dataframe



    def _get_all_rss_feed_urls(self, given_source):
        """Get the rss feed urls for a source

        Args:
            source (String): source from the dataframe.
        
        Returns:
            source_and_category (List[Dict[str, str]]): A dictonary of source rss links and its categories.
        """
        dataframe = self._load_dataframe()

        source_dataframe = dataframe[dataframe["sources"] == given_source]
        source_category = []
        for index, row in source_dataframe.iterrows():
            source_category.append(
                {   
                    "link": row['link'],
                    "category": row['category'],
                    "source": given_source,
                }
            )

        if not source_category:
            raise ValueError("No source_category found")
        
        return source_category


 

            


    