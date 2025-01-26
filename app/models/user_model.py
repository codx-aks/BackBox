from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self):
        super().__init__()
    
    # Add User-specific methods here
    def find_by_email(self, email):
        return self.collection.find_one({'email': email}, {'_id': 0})