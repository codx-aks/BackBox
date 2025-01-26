from app.models.base_model import BaseModel
from datetime import datetime
from bson import ObjectId

class Manager(BaseModel):
    def __init__(self):
        super().__init__()
    
    def create_manager(self, manager_data):
        manager = {
            'name': manager_data['name'],
            'email': manager_data['email'],
            'phone': manager_data['phone'],
            'designation': manager_data['designation'],
            'employee_id': manager_data['employee_id'],
            'department': manager_data['department'],
            'project_id': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.insert_one(manager)
    
    def assign_project(self, manager_id, project_id):
        return self.update_one(
            {'_id': ObjectId(manager_id)},
            {'project_id': project_id, 'updated_at': datetime.utcnow()}
        )
    
    def get_manager_project(self, manager_id):
        return self.find_one({'_id': ObjectId(manager_id)})