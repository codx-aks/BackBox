from app.models.project_model import Project
from app.models.manager_model import Manager
from app.models.cctv_model import CCTV
from datetime import datetime

class ProjectController:
    def __init__(self):
        self.project_model = Project()
        self.manager_model = Manager()
        self.cctv_model=CCTV()
    
    def initialize_project(self, project_data, manager_id=None):
        """
        Initialize a new project and optionally assign to manager
        """
        try:

            required_fields = [
                'name', 
                'centre_lat', 
                'centre_long', 
                'location', 
                'project_code'
            ]
            
            for field in required_fields:
                if field not in project_data:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }
            
            # Add manager_id if provided
            if manager_id:
                project_data['manager_id'] = manager_id
            
            # Create project
            project_id = self.project_model.create_project(project_data)
            
            if project_id:
                # If manager_id is provided, update manager with project_id
                if manager_id:
                    self.manager_model.update_one(
                        {'_id': manager_id},
                        {'project_id': project_id, 'updated_at': datetime.utcnow()}
                    )
                
                return {
                    "status": "success",
                    "message": "Project initialized successfully",
                    "project_id": project_id
                }
            return {
                "status": "error",
                "message": "Failed to initialize project"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def configure_project(self, project_id, config_data):
        try:
            # Validate required fields
            required_fields = [
                'siteTopLeft', 
                'siteBottomRight', 
                'hazardousZones', 
                'cctvCoverage',
                'sea_level_ground_elevation',
                'danger_elevation',
                'number_of_floors',
                'floor_height'
            ]
            
            for field in required_fields:
                if field not in config_data:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }

            # Create CCTV entries
            cctv_ids = self.cctv_model.create_cctvs(config_data['cctvCoverage'])
            config_data['cctv_ids'] = cctv_ids

            # Update project configuration
            result = self.project_model.configure_project(project_id, config_data)
            
            if result:
                return {
                    "status": "success",
                    "message": "Project configured successfully",
                    "cctv_count": len(cctv_ids)
                }
            return {
                "status": "error",
                "message": "Failed to update project configuration"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def assign_manager(self, project_id, manager_id):
        """
        Assign a manager to a project
        """
        try:
            # Update project with manager_id
            project_result = self.project_model.update_one(
                {'_id': project_id},
                {'manager_id': manager_id, 'updated_at': datetime.utcnow()}
            )
            
            # Update manager with project_id
            manager_result = self.manager_model.update_one(
                {'_id': manager_id},
                {'project_id': project_id, 'updated_at': datetime.utcnow()}
            )
            
            if project_result and manager_result:
                return {
                    "status": "success",
                    "message": "Manager assigned to project successfully"
                }
            return {
                "status": "error",
                "message": "Failed to assign manager to project"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }