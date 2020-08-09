from scheduler import Scheduler
import schedule
from motivational import MotivationalNews
from database import FirebaseDB
import time
from top_stories import TopStories
import logging 
from quote import GetQuote


logger = logging.getLogger(__name__)

# initilize database once
firebase = FirebaseDB()
logger.info("Database init complete")

def push_quote():
    quote_object = GetQuote()
    quote = quote_object.get_quote()
    kvell_db = firebase.kvell_database()
    kvell_db.child('quote_of_the_day').remove()
    kvell_db.child('quote_of_the_day').set(quote)

def main():
    scheduler = Scheduler()
    motivational = MotivationalNews()
    top_stories = TopStories()

    # collect all the data
    news_data = scheduler.get_all_news_data()
    logger.info("All news data collected")
    data_for_push, categories = scheduler.data_to_push_firebase(news_data)
    motivational_news_data = motivational.data_to_push_firebase()
    top_stories_news = top_stories.data_to_push_firebase()
    logger.info("Data ready to be pushed")
    start_time = time.time()
    # remove the old data populated int the database
    #scheduler.scheduled_delete(firebase.kvell_database())
    logger.info("Data deleted")
    
    # populate the database
    scheduler.scheduled_push(firebase.kvell_database(), data_for_push, categories, motivational_news_data, top_stories_news)
    logger.info("Data pushed")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
   # push_quote()
    # schedule.every().hour.do(main)
    # schedule.every().day.at("00:00").do(push_quote)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
