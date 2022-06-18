import pymongo

from dependency.database.database import DatabaseWrapper

DATABASE_WRAPPER_INSTANCE=None

def getDatabaseWrapperInstance():
    global DATABASE_WRAPPER_INSTANCE
    if not DATABASE_WRAPPER_INSTANCE:
        username="sujan079"
        password="hswOC3XWnnWMYJe0"
        database="reddit_db"
        url=f"mongodb+srv://{username}:{password}@databasecluster.svz8u.mongodb.net/"
        client=pymongo.MongoClient(url)
        db=client[database]
        DATABASE_WRAPPER_INSTANCE = DatabaseWrapper(db=db)
    return DATABASE_WRAPPER_INSTANCE
