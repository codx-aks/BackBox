from app.models.manager_model import Manager
from datetime import datetime

class ManagerController:
    def __init__(self):
        self.manager_model = Manager()
    
    def create_manager(self, manager_data):
        try:
            # Validate required fields
            required_fields = ['name', 'email', 'phone', 'designation', 'employee_id', 'department']
            for field in required_fields:
                if field not in manager_data:
                    return {"status": "error", "message": f"Missing required field: {field}"}
            
            # Add timestamps
            manager_data['created_at'] = datetime.utcnow()
            manager_data['updated_at'] = datetime.utcnow()
            manager_data['project_id'] = None  # Initialize with no project
            
            manager_id = self.manager_model.create_manager(manager_data)
            return {
                "status": "success",
                "message": "Manager created successfully",
                "manager_id": manager_id
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_manager_project(self, manager_id):
        try:
            manager = self.manager_model.get_manager_project(manager_id)
            if manager:
                return {
                    "status": "success",
                    "data": manager
                }
            return {
                "status": "error",
                "message": "Manager not found"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}