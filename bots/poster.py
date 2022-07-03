import random
from dependency.logger.index import getLoggerInstance
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
from datetime import datetime

def pin_to_profile(reddit,account):
    db=getDatabaseWrapperInstance()
    if not "pinned" in account:
        account["pinned"]=False
    
    if not account["pinned"]:
        print("Pinning")
        reddit.pin_to_post(subreddit=account["username"],title='Watch me dildo play for free ;)\)',url="https://downloadlocked.com/cl/v/gvxjr")
        db.update_by_id(collection="accounts",id=account["_id"],value={"pinned":True})

def make_post(author,account):
    logger=getLoggerInstance("poster_logger")
    
    log_data={
        "username":account["username"],
        "password":account["password"],
        "subreddit":"",
        "post":"",
        "date":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "message":""
    }

    reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
    print("POSTING USING")
    print(f"USERNAME:{account['username']}\nPASSWORD:{account['password']}")
            
    db=getDatabaseWrapperInstance()
    subreddits=reddit.get_subreddits_by_type("nsfw")
    posts=db.find_all("posts",{"author":author})
    
    post=random.choice(posts)

    pin_to_profile(reddit=reddit,account=account)
    if not "posted_on" in post:
        post["posted_on"]=[]

    posted_on=post["posted_on"] #gets the subreddits that the account posted on 
    print(f"Previous Posts{posted_on}")
    for sub in subreddits:
        log_data["post"]=post["_id"]
        log_data["subreddit"]=sub
        
        if not sub in posted_on:            
            print(f"Posting on {sub}")
            try:

                if not reddit.get_account_banned_status():
                    reddit.post_with_title_url(subreddit=sub,title=post["title"],url=post["url"])
                    
                    log_data["message"]=f"Posted Successfully on {sub}"

            except Exception as e:
                print(f"Error Posting to {sub}\\title:{post['title']}\nurl:{post['url']} ")

                log_data["message"]=f"Error Posting to {sub}\\title:{post['title']}\nurl:{post['url']} "

                if "403" in str(e):
                    db.update_by_id("accounts",id=account["_id"],value={"isBanned":True})
            finally:
                posted_on.append(sub)
                db.update_by_id(collection="posts",id=post["_id"],value={"posted_on":posted_on})
                logger.dispatchLog(data=log_data) 
                return # breaks out of the function

        else:
            log_data["message"]=f"Not Posted on {sub} because already posted. Prev Post {posted_on}"
            logger.dispatchLog(data=log_data) 

def get_account_active_status(account):
    if account:    
        if not "isActive" in account:
            return False
        return account["isActive"]
    return False

def assign_author(author):
    print(f"Assigning {author} to a account")
    db=getDatabaseWrapperInstance()
    accounts=db.find_all(collection="accounts")
    account=random.choice(accounts)
    while True:
        if not "author" in account:
            break 
        if "author" in account:
            if not account["author"]:
                break
        account=random.choice(accounts)
    db.update_by_id(collection="accounts",id=account["_id"],value={"author":author})
    print(f"Assigning {author} to a account {account['username']}")

    return True

def run():
    print("Starting Posting")
    db=getDatabaseWrapperInstance()
    authors=db.get_distinct("posts","author")
    author=random.choice(authors)

    account=db.find_one("accounts",{"author":author})

    if not account:
        author_assigned=assign_author(author)
        if author_assigned:
            account=db.find_one("accounts",{"author":author})

    print(f"Current Account {account['username']}->Current Author {author}")


    # db.update_by_id(collection="accounts",id=account["_id"],value={"isActive":True}) #represents the bot being active
    
    make_post(author=author,account=account)
    
    # db.update_by_id(collection="accounts",id=account["_id"],value={"isActive":False})#represents the bot being inactive



    print("Ended")