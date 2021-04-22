from datetime import datetime
import uuid
from time import sleep
import logging
import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing.pool import ThreadPool
import threading

from dao.database_mongo import get_connection
from service.server import run


url = "https://www.reddit.com/top/?t=month"

enough_posts_number = 7
enough_result_posts = 4
enough_update_times = 3

PAUSE = 3


def load_data():
    """Read the .env file"""

    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
    except Exception:
        logging.exception("Can't find the .env file")


def get_driver():
    """Return selenium driver using Chrome"""

    thread_local = threading.local()
    driver = getattr(thread_local, 'driver', None)

    print("LOOKING FOR DRIVER...")

    while driver is None:

        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            capabilities = options.to_capabilities()
            driver = webdriver.Remote(
                command_executor='http://hub:4444/wd/hub',
                desired_capabilities=capabilities)
            sleep(3)
            setattr(thread_local, 'driver', driver)
            driver.get(url)
        except Exception as e:
            print("LOOKING FOR DRIVER...")
            continue

    print("CHROME WEB DRIVER FORMED SUCCESSFULLY")

    return driver


def form_date(*args):
    """Form the creation date"""

    if args:
        year, month, day, hour, minute = args
    else:
        date = datetime.now()

        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute

    dt = datetime(year, month, day, hour, minute)

    return dt.strftime("%Y%m%d%H%M")


def form_file_name():
    """Form the file name"""

    return datetime.now().strftime("reddit-%Y%m%d%H%M")


def scroll(counter):
    """Infinity scroll"""

    for _ in range(counter):
        DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight); ")
        sleep(PAUSE)


def get_page(updates):
    """Get html context"""

    scroll(updates)

    return DRIVER.page_source


def get_post_list(updates):
    """Form post list to scrap"""

    html = get_page(updates)
    soup = BeautifulSoup(html, "lxml")

    return soup.select(".Post")[:enough_posts_number]


def get_author(post):
    """Get reddit post author"""

    return post.select(CLASSES["author"])[0].get_text()


def get_post_date(post):
    """Get reddit post date"""

    return post.select((CLASSES["post_date"]))[0].get_text()


def get_post_url(post):
    """Get reddit post url"""

    return f'https://www.reddit.com{post.find_all("a", class_=CLASSES["post_url"])[0].get("href")}'


def get_number_of_comments(post):
    """Get reddit number of comments of post"""

    return post.select(CLASSES["number_of_comments"])[0].get_text()


def get_number_of_votes(post):
    """Get reddit number of votes of post"""

    return post.select(CLASSES["number_of_votes"])[0].get_text()


def get_post_category(post):
    """Get reddit post category"""

    return post.find_all('a', class_=CLASSES["post_category"])[0].get('href').split('/')[-2]


def get_user_info(author):
    """Get reddit profile info"""

    user_url = f"https://www.reddit.com/user/{author}"
    user_gilded_url = f"https://old.reddit.com/user/{author}/gilded"
    DRIVER.get(user_url)
    user_html = DRIVER.page_source
    DRIVER.get(user_gilded_url)
    user_gilded_html = DRIVER.page_source
    user_soup = BeautifulSoup(user_html, 'lxml')
    user_gilded_soup = BeautifulSoup(user_gilded_html, 'lxml')

    user_karma = user_soup.select(CLASSES["user_karma"])
    user_comment_karma = user_gilded_soup.select(CLASSES["user_comment_karma"])
    post_karma = user_gilded_soup.select(CLASSES["post_karma"])

    if len(user_karma) == 0 or len(user_comment_karma) == 0 or len(post_karma) == 0:  # private profile or adult
        # only (we can't reach)
        return (0,) * 4

    user_comment_karma = user_comment_karma[0].get_text()
    post_karma = post_karma[0].get_text()
    user_karma = user_karma[0].get_text()
    user_cake_day = user_soup.select(CLASSES["user_cake_day"])[0].get_text()

    return user_karma, user_comment_karma, user_cake_day, post_karma


def scrap(updates):
    """Scrapping info from reddit"""

    print("START SCRAPING...")

    result = []

    context = get_post_list(updates)

    for post in context:
        if len(result) == enough_result_posts:
            break

        uid = uuid.uuid1().hex

        author = get_author(post)

        if author.startswith("t3"):  # ads
            continue

        author = author[2:]

        post_date = get_post_date(post)
        post_url = get_post_url(post)

        number_of_comments = get_number_of_comments(post)
        number_of_votes = get_number_of_votes(post)
        post_category = get_post_category(post)

        user_karma, user_comment_karma, user_cake_day, post_karma = get_user_info(author)

        if not user_karma:
            continue

        result.append({"uid": uid,
                       "post_date": post_date,
                       "post_url": post_url,
                       "number_of_comments": number_of_comments,
                       "number_of_votes": number_of_votes,
                       "post_category": post_category,
                       "author": author,
                       "user_karma": user_karma.replace(" ", "."),
                       "post_karma": post_karma.replace(" ", "."),
                       "user_comment_karma": user_comment_karma.replace(" ", "."),
                       "user_cake_day": user_cake_day.split()[0]})

    print("SCRAPING COMPLETE!")

    return result


def form_logging():
    """Create instance of log file"""

    filename = form_file_name()
    logging.basicConfig(filename=f"log-{filename}.log", level=logging.INFO)


def main():
    """Form the file"""

    posts = []
    form_logging()

    try:
        posts = scrap(enough_update_times)
    except Exception:
        logging.exception("An error has happened while forming posts list!")
    else:
        logging.info("Posts list has been formed successfully!")

    try:
        print("CONNECT TO DB...")
        posts_col, users_col = get_connection()
        
        posts_count = posts_col.find({}).count_documents()
        users_count = users_col.find({}).count_documents()

        if posts_count or users_count:
            posts_col.delete_many({})
            users_col.delete_many({})
            
        for post in posts:
            for_post = {"uid": post["uid"],
                        "post_url": post["post_url"],
                        "post_date": post['post_date'],
                        "author": post['author'],
                        "number_of_comments": post['number_of_comments'],
                        "number_of_votes": post['number_of_votes'],
                        "post_category": post['post_category']
            }
            for_user = {"username":post['author'],
                        "user_cake_day":post['user_cake_day'],
                        "user_karma":post['user_karma'],
                        "post_karma":post['post_karma'],
                        "comment_karma":post['user_comment_karma']

            }

            posts_col.insert_one(for_post)
            users_col.insert_one(for_user)
        print("Records inserted successfully!")
        logging.info("Records inserted successfully!")
    except Exception as e:
        print(e)
        logging.exception("An error has happened while inserting into database!")

    logging.info("Program finished!")

    run("mongo")


DRIVER = get_driver()
load_data()
CLASSES = {
    "author": os.environ.get("author"),
    "post_date": os.environ.get("post_date"),
    "post_url": os.environ.get("post_url"),
    "number_of_comments": os.environ.get("number_of_comments"),
    "number_of_votes": os.environ.get("number_of_votes"),
    "post_category": os.environ.get("post_category"),
    "user_karma": os.environ.get("user_karma"),
    "user_comment_karma": os.environ.get("user_comment_karma"),
    "post_karma": os.environ.get("post_karma"),
    "user_cake_day": os.environ.get("user_cake_day"),
}

if CLASSES["author"] is None:
    form_logging()

    logging.error("Can't reach the data of .env file")
    raise Exception

if __name__ == "__main__":
    ThreadPool(10).apply(main)
