import time
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
import random

def run():
    db=getDatabaseWrapperInstance()
    reddit_accounts=db.find_all("accounts")
    reddit_accounts=random.sample(reddit_accounts,len(reddit_accounts))

    if len(reddit_accounts)>0:
        account=reddit_accounts[0]
        reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
        print("POSTING USING")
        print(f"USERNAME:{account['username']}\nPASSWORD:{account['password']}")

        
        subreddits=reddit.get_subreddits_by_type("nsfw")
        posts=reddit.get_posts()

        posts=random.sample(posts,len(posts))


        for post in posts:
            for index,sub in enumerate(subreddits):


                print(f"Posting on {sub}")
                try:

                    if not reddit.get_account_banned_status():
                        reddit.post_with_title_url(subreddit=sub,title=post["title"],url=post["url"])
                    else:
                        pass

                except Exception as e:
                    print(f"Error Posting to {sub}\\title:{post['title']}\nurl:{post['url']} ")
                    print(e)
                time.sleep(12*60)
