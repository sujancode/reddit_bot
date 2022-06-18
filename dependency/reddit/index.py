import praw
import json
from dependency.database.index import getDatabaseWrapperInstance

from dependency.reddit.reddit import RedditWrapper

REDDIT_WRAPPER_INSTANCE=None


def getRedditWrapperInstance(username="",password="",client_id="",client_secret=""):
    global REDDIT_WRAPPER_INSTANCE
    db=getDatabaseWrapperInstance()
    RedditClient=""
    try:
        RedditClient=praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=username.strip()
        )
    except Exception as e:
        print(e)

    if not REDDIT_WRAPPER_INSTANCE:
        REDDIT_WRAPPER_INSTANCE = RedditWrapper(reddit=RedditClient,json=json,db=db) 
    return REDDIT_WRAPPER_INSTANCE