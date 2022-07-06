import random
from dependency.logger.index import getLoggerInstance
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
from datetime import datetime
import os

titles=[
    "Every upvote gets a video in your inbox comment to let me know you've done it", 
    "You UPVOTE, I send a FREE NUDE PACK! Comment ‘done’ I’ve sent thousands",
    "Upvote for a blowjob video and nude pack in your DMs, Remember to tell me when you’re done",
    "Upvote = Free pack nude, Comment DONE", 
    "Upvote and comment \"Done\" for FREE 100+ Nudes, just try and get surprised",
    "1 upvote = 1 FREE NUDE PACK OR VIDEO Comment DONE",
    "Upvote for 5 instant nudes, autoreply is on!",
    "I put my inbox on auto-reply so who gives me an upvote will get instantly a nude and surprise",
    "there's no such thing as auto reply on reddit but if you upvote and comment i promise i'll send the full vid",
    "Upvote for a free video in your DM, instant",
    "EVERY upvote will get MY sex tape",
    "Every Upvote gets my ANAL VID in dm's, I promise",
    "1 upvote=5 nudes in your dm If u active, I give a little surprise",
    "I want to make a deal with you, 1 upvote =25 video and 50 picture in your dm,try me",
    "Upvote for 10 free nudes in your DM’s",
    "Upvote for nudes !! I actually send",
    "One upvote = my sextape in your dms",
    "1 upvote= 7 nudes in your DM, instant",
    "Sending my sextape to whoever upvotes just because i’m horny (my autoreply is on!)",
    "Every Single Upvote Gets 10 Free Nudes In Dms! Try me!",
    "Upvote and you will receive a prize in your DM",
    "Every upvote gets a video of me rubbing my pussy",
    "EVERY UPVOTE gets 4 free pussy pics, TRY ME"
]

def stop_instance():
    os.system("sudo shutdown now -h")

def pin_to_profile(reddit,account):
    db=getDatabaseWrapperInstance()
    if not "pinned" in account:
        account["pinned"]=False
    
    if not account["pinned"]:
        print("Pinning")
        reddit.pin_to_post(subreddit=account["username"],title='My free pussy play videos for you 💋',url="https://downloadlocked.com/fl/3qy32")
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
    for post in posts:    
        print(post["title"])
        posted_on=[]
        if "posted_on" in post:
            posted_on=post["posted_on"] #gets the subreddits that the account posted on 
        print(f"Previous Posts{posted_on}")

        pin_to_profile(reddit=reddit,account=account)



        for sub in subreddits:
            log_data["post"]=post["_id"]
            log_data["subreddit"]=sub
            
            if not sub in posted_on:            
                print(f"Posting on {sub}")
                try:

                    if not reddit.get_account_banned_status():
                        title=random.choice(titles)# post["title"]

                        reddit.post_with_title_url(subreddit=sub,title=title,url=post["url"])
                        
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

##This shit no use

# def assign_author(author):
#     print(f"Assigning {author} to a account")
#     db=getDatabaseWrapperInstance()
#     accounts=db.find_all(collection="accounts",filter={"author":""})
#     if len(accounts)>0:
#         for account in accounts:
#             if not "author" in account:
#                 db.update_by_id(collection="accounts",id=account["_id"],value={"author":author})
#                 print(f"Assigning {author} to a account {account['username']}") 
#                 break
#             if "author" in account:
#                 if not account["author"]:
#                     db.update_by_id(collection="accounts",id=account["_id"],value={"author":author})
#                     print(f"Assigning {author} to a account {account['username']}") 
#                     break
#         return True
#     else:
#         return False

def run():
    print("Starting Posting")
    db=getDatabaseWrapperInstance()
    authors=db.get_distinct("posts","author")
    author=random.choice(authors)

    account=db.find_one("accounts",{"author":author})
    
    make_post(author=author,account=account)
    
    stop_instance()


    print("Ended")