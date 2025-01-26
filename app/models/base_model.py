from app.extensions import db
from bson import ObjectId

class BaseModel:
    def __init__(self):
        if db is None:
            raise Exception("Database connection is not initialized.")
        self.collection = db[self.__class__.__name__.lower()]
    
    def test_connection(self):
        try:
            db.client.admin.command('ping')
            return True
        except Exception as e:
            return str(e)
    
    def insert_one(self, data):
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            return str(e)
    
    def find_all(self):
        try:
            return list(self.collection.find({}, {'_id': 0}))
        except Exception as e:
            return str(e)
    
    def find_by_id(self, id):
        try:
            if isinstance(id, str):
                id = ObjectId(id)
            return self.collection.find_one({'_id': id}, {'_id': 0})
        except Exception as e:
            return str(e)
    
    def find_one(self, query):
        try:
            if '_id' in query and isinstance(query['_id'], str):
                query['_id'] = ObjectId(query['_id'])
            return self.collection.find_one(query, {'_id': 0})
        except Exception as e:
            return str(e)

    def update_one(self, query, update_data):
        try:
            if isinstance(query, str):
                query = {'_id': ObjectId(query)}
            elif '_id' in query and isinstance(query['_id'], str):
                query['_id'] = ObjectId(query['_id'])
            
            result = self.collection.update_one(
                query,
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            return str(e)
    
    def delete_one(self, query):
        try:
            if isinstance(query, str):
                query = {'_id': ObjectId(query)}
            elif '_id' in query and isinstance(query['_id'], str):
                query['_id'] = ObjectId(query['_id'])
            
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            return str(e)
    
    def find_many(self, query=None, projection=None):
        try:
            if query is None:
                query = {}
            if projection is None:
                projection = {'_id': 0}
            
            if '_id' in query and isinstance(query['_id'], str):
                query['_id'] = ObjectId(query['_id'])
                
            return list(self.collection.find(query, projection))
        except Exception as e:
            return str(e)