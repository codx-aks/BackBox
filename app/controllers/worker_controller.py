from app.models.worker_model import Worker
from datetime import datetime

class WorkerController:
    def __init__(self):
        self.worker_model = Worker()
    
    def create_worker(self, worker_data):
        try:
            # Validate required fields
            required_fields = ['worker_name', 'social_security_number', 'phone_number']
            for field in required_fields:
                if field not in worker_data:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }
            
            # Create worker
            worker_id = self.worker_model.create_worker(worker_data)
            
            if worker_id:
                # Get the created worker to return watch_id
                worker = self.worker_model.find_by_id(worker_id)
                return {
                    "status": "success",
                    "message": "Worker created successfully",
                    "worker_id": worker_id,
                    "watch_id": worker.get('watch_id')
                }
            return {
                "status": "error",
                "message": "Failed to create worker"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def update_worker_data(self, worker_data):
        """
        Update worker's data including location, heart rate, and elevation
        """
        try:
            # Validate required fields
            required_fields = ['watch_id', 'latitude', 'longitude', 'heart_rate', 'absolute_elevation']
            for field in required_fields:
                if field not in worker_data:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }

            # Validate data types
            try:
                watch_id = int(worker_data['watch_id'])
                float(worker_data['latitude'])
                float(worker_data['longitude'])
                int(worker_data['heart_rate'])
                float(worker_data['absolute_elevation'])
            except ValueError:
                return {
                    "status": "error",
                    "message": "Invalid data types. Please check your input values"
                }

            # Validate ranges
            if not (-90 <= float(worker_data['latitude']) <= 90):
                return {
                    "status": "error",
                    "message": "Latitude must be between -90 and 90"
                }
                
            if not (-180 <= float(worker_data['longitude']) <= 180):
                return {
                    "status": "error",
                    "message": "Longitude must be between -180 and 180"
                }
                
            if not (0 <= int(worker_data['heart_rate']) <= 250):
                return {
                    "status": "error",
                    "message": "Heart rate must be between 0 and 250"
                }

            # Check if worker exists
            worker = self.worker_model.get_worker_by_watch_id(watch_id)
            if not worker:
                return {
                    "status": "error",
                    "message": f"No worker found with watch_id: {watch_id}"
                }

            # Update worker data
            result = self.worker_model.update_worker_data(watch_id, worker_data)
            
            if result:
                return {
                    "status": "success",
                    "message": "Worker data updated successfully",
                    "watch_id": watch_id,
                    "data": {
                        "location": {
                            "latitude": float(worker_data['latitude']),
                            "longitude": float(worker_data['longitude'])
                        },
                        "heart_rate": int(worker_data['heart_rate']),
                        "absolute_elevation": float(worker_data['absolute_elevation'])
                    }
                }
            return {
                "status": "error",
                "message": "Failed to update worker data"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_all_workers(self):
        try:
            workers = self.worker_model.get_all_workers()
            return {
                "status": "success",
                "workers": workers
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    def get_worker_by_watch_id(self, watch_id):
        try:
            worker = self.worker_model.get_worker_by_watch_id(watch_id)
            if worker:
                return {
                    "status": "success",
                    "worker": worker
                }
            return {
                "status": "error",
                "message": f"No worker found with watch_id: {watch_id}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }