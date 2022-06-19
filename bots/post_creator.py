
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
from dependency.imgur.index import getImgurWrapperInstance

import json


def assign_author(author):
    db=getDatabaseWrapperInstance()
    accounts=db.find_all("accounts")
    for account in accounts:
        if "author" in account:
            if not account["author"]:
                db.update_by_id(collection="accounts",id=account["_id"],value={"author":author})
                break
        else:
            print("Author Already Assigned")
        



def run():
    db=getDatabaseWrapperInstance()
    reddit_accounts=db.find_all("accounts")
    account=None

    if len(reddit_accounts)>0:
        account=reddit_accounts[0]
        reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
        imgur=getImgurWrapperInstance()

        subreddits=["realgirls"]

        for sub in subreddits:
            posts=(reddit.scrape_top_posts_from_subreddit(sub))
            
            for post in posts:
                print(f"{post.author}")
                author=post.author
                top_posts=reddit.get_top_post_of_account(author)  
                print(len(top_posts))
                for top in top_posts:
                    print(f"{top.title},{top.url}")
                    upload_image=imgur.upload_to_imgur(top.url)
                    
                    if upload_image:
                        upload_image=json.loads(upload_image)

                        data={
                            "url":upload_image['data']['link'],
                            "title":top.title,
                            "author":str(author)
                        }
                        db.insert("posts",data=data)
                        assign_author(author=str(author))

