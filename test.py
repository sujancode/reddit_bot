from dependency.database.index import getDatabaseWrapperInstance
from dependency.reddit.index import getRedditWrapperInstance

db=getDatabaseWrapperInstance()

# accounts=db.find_all("accounts")

# for account in accounts:
#     print(account)
#     db.update_by_id(collection="accounts",id=account["_id"],value={"author":""})

posted_users=db.get_distinct("poster_logger",field_name="username")

print(posted_users)
# for user in posted_users:
#     try:
#         print(user)
#         account=db.find_one(collection="accounts",filter={"username":user})
#         print(account)
#         reddit=getRedditWrapperInstance(username=account["username"],password=account["password"],client_id=account["client_id"],client_secret=account["client_secret"],create_new_instance=True)
#         reddit.delete_all_submission(username=user)
#         db.delete_by_id("accounts",id=account["_id"])
#     except:
#         print("No Account")
        


for post in db.find_all(collection="posts"):
    db.update_by_id(collection="posts",id=post["_id"],value={"posted_on":[]}) 

# for account in db.find_all(collection="accounts"):
#     print(account)
#     db.update_by_id(collection="accounts",id=account["_id"],value={"author":""}) 

# print(db.get_distinct("posts",field_name="author"))