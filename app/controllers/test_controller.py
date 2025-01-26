from app.models.test_model import Test

class TestController:
    def __init__(self):
        self.test_model = Test()
    
    def test_db_connection(self):
        result = self.test_model.test_connection()
        if result is True:
            return {"status": "success", "message": "Successfully connected to MongoDB"}
        return {"status": "error", "message": str(result)}
    
    def create_test_document(self, data):
        result = self.test_model.insert_one(data)
        return {"status": "success", "inserted_id": result}
    
    def get_all_documents(self):
        result = self.test_model.find_all()
        return {"status": "success", "data": result}