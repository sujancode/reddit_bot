
class DatabaseWrapper:
    def __init__(self,db) -> None:
        self.db=db
        
    def insert(self,collection,data):
        collection=self.db[collection]
        return collection.insert_one(data)

    def find_one(self,collection,filter):
        collection=self.db[collection]
        return collection.find_one(filter)
    
    def find_all(self,collection):
        collection=self.db[collection]
        return [item for item in collection.find()]