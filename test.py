from dependency.database.index import getDatabaseWrapperInstance
from dependency.reddit.index import getRedditWrapperInstance

db=getDatabaseWrapperInstance()

posted_users=db.get_distinct("poster_logger",field_name="username")

print(posted_users)
for user in posted_users:
    print(user)
    account=db.find_one(collection="accounts",filter={"username":user})
    print(account)
    reddit=getRedditWrapperInstance(username=account["username"],password=account["password"],client_id=account["client_id"],client_secret=account["client_secret"],create_new_instance=True)
    reddit.delete_all_submission(username=user)