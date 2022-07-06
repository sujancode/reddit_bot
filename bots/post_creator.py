
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
from dependency.imgur.index import getImgurWrapperInstance

import json


def assign_author(accounts,authors):
    for index,author in enumerate(authors):
        db=getDatabaseWrapperInstance()
        account=accounts[index]
        db.update_by_id(collection="accounts",id=account["_id"],value={"author":author})
        



def run():
    db=getDatabaseWrapperInstance()
    reddit_accounts=db.find_all(collection="accounts",filter={"author":""})
    account=None

    if len(reddit_accounts)>0:
        account=reddit_accounts[0] #doesnot Matter What Account Is chosen only need for scrapping
        reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
        imgur=getImgurWrapperInstance()

        subreddits=["BarelyLegalTeens","RealGirls"]

        authors=set({})

        for sub in subreddits:
            posts=(reddit.scrape_top_posts_from_subreddit(sub))
            
            for post in posts:
                author=post.author
                authors.add(str(author))
            if len(authors)==len(reddit_accounts):
                break
        assign_author(authors=authors,accounts=reddit_accounts)

        for author in authors:
            top_posts=reddit.get_top_post_of_account(author=author)
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

