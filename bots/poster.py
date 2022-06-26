import time
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance



def make_post(author,reddit):
    db=getDatabaseWrapperInstance()
    subreddits=reddit.get_subreddits_by_type("nsfw")
    posts=db.find_all("posts",{"author":author})

    for post in posts:
        for index,sub in enumerate(subreddits):


            print(f"Posting on {sub} using ip {reddit.get_ip()}")
            try:

                if not reddit.get_account_banned_status():
                    reddit.post_with_title_url(subreddit=sub,title=post["title"],url=post["url"])
                else:
                    pass

            except Exception as e:
                print(f"Error Posting to {sub}\\title:{post['title']}\nurl:{post['url']} ")
                print(e)
            time.sleep(12*60)

def run():
    db=getDatabaseWrapperInstance()
    authors=db.get_distinct("posts","author")
    for author in authors:
        print(author)
        account=db.find_one("accounts",{"author":author})
        print(account)
        reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
        print("POSTING USING")
        print(f"USERNAME:{account['username']}\nPASSWORD:{account['password']}")
        make_post(author=author,reddit=reddit)

    
