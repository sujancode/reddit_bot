
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
from dependency.imgur.index import getImgurWrapperInstance


import json



    
def run():
    db=getDatabaseWrapperInstance()
    reddit_accounts=db.find_all("accounts")
    account=None

    if len(reddit_accounts)>0:
        account=reddit_accounts[0]
        reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
        imgur=getImgurWrapperInstance()

        subreddits=reddit.get_subreddits_by_type("nsfw")

        for sub in subreddits:
            posts=(reddit.scrape_top_posts_from_subreddit(sub))
            
            for post in posts:
                
                upload_image=imgur.upload_to_imgur(post.url)
                
                if upload_image:
                    upload_image=json.loads(upload_image)
                    print(upload_image)

                    data={
                        "url":upload_image['data']['link'],
                        "title":post.title
                    }
                    db.insert("posts",data=data)
                

