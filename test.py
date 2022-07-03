from dependency.database.index import getDatabaseWrapperInstance

db=getDatabaseWrapperInstance()

posted_users=db.get_distinct("poster_logger",field_name="username")

print(posted_users)