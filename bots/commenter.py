import time
from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance
import praw

pitch="Check out my dildo play here. u/GuideOk4874"
def make_comment(subreddit,reddit):
    comments=reddit.get_top_subreddit_comments(subreddit)
    comments_replied_to=[]
    for comment in comments:
        try:
            print(f"Replying to {comment.body}")

            if comment.body and comment.id not in comments_replied_to and comment.author != reddit.get_current_user():
                comment.reply(pitch)
                reddit.reply_to_comment(comment,pitch)
                comments_replied_to.append(comment.id)
                time.sleep(10)
        except praw.exceptions.APIException as exception:
            print(f"Error Replying {comment.body}")
            for subexception in exception.items:
                if subexception.error_type=="RATELIMIT":
                    print("Rate Limit Encountered")
                    print(exception)
                    wait_for=str(subexception).replace('RATELIMIT: "Looks like you\'ve been doing that a lot. Take a break for ',"")
                    if "minute" in wait_for:
                        wait_for=wait_for[0:2]
                        print(f"Wating For {wait_for}")
                        time.sleep(int(wait_for)*60)
                    elif "seconds" in wait_for:
                        wait_for=wait_for[0:2]
                        print(f"Wating For {wait_for}")
                        time.sleep(int(wait_for))

def run():
    db=getDatabaseWrapperInstance()
    accounts=db.find_all("accounts")
    for account in accounts:
        print(account)
        reddit=getRedditWrapperInstance(username=account['username'],password=account['password'],client_id= account['client_id'],client_secret=account['client_secret'])
        print("Comment USING")
        print(f"USERNAME:{account['username']}\nPASSWORD:{account['password']}")

        subreddits=reddit.get_subreddits_by_type("nsfw")
        
        for sub in subreddits:
            print(f"Making comments on {sub}")

            make_comment(subreddit=sub,reddit=reddit)
